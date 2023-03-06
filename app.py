"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def index():
    '''show list of posts, most-recent first'''
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/homepost.html' posts=posts)

# ADD error handler with custom error html page

################################################################################################
# User route

@app.route('/users')
def user_list():
    '''Show all users'''
    users = user.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user():
    '''Show form for new user'''
    return render_template('users/newuserform.html')

@app.route('/users/new', methods = ['POST'])
def create_user():
    '''Process add form, adding new user and going back to users'''
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    new_user = User(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    '''show info about given user'''
    user = User.query.get_or_404(user_id)
    return render_template('users/userDetails.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    '''show edit form'''
    user = User.query.get_or_404(user_id)
    return render_template('users/userEdit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    '''process the edit form, returning the user to the /users page'''
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    new_user = User(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:users_id>/delete', methods=["POST"])
def delete_user(user_id):
    '''Handle form submission for deleting an existing user'''
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

#################################################################################
# Posts route

@app.route('/users/<int:user_id/posts/newpost')
def posts_new_form(user_id):
    '''show a form to create post for current user'''
    user = User.query.get_or_404(user_id)
    return render_template("posts/newpost.html", user = user)

@app.route('/users/<int:user_id/posts/newpost', methods=['POST'])
def post_new(user_id):
    '''form submission for new post creation for current user'''

    user = User.query.get_of_404(user_id)
    new_post = Post(title= request.form['title'],
                    content= request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f'/users/{user_id}')

@app.route('posts/<int:post_id>')
def posts_show(post_id):
    '''show a post and buttons to delete and edit the post'''
    post = Post.query.get_of_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission/ updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission/ deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")