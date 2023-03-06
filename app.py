"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "itsasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def index():
    '''show list of posts, most-recent first'''
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('/posts/homepage.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    '''show 404 page'''
    return render_template('404.html'), 404

################################################################################################
# User route

@app.route('/users')
def user_list():
    '''Show all users'''
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user():
    '''Show form for new user'''
    return render_template('/users/newuserform.html')

@app.route('/users/new', methods = ['POST'])
def create_user():
    '''Process add form, adding new user and going back to users'''
    new_user = User(first_name = request.form['first_name'],
                    last_name = request.form['last_name'],
                    image_url = request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    flash(f'User {new_user.full_name} added.')

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    '''show info about given user'''
    user = User.query.get_or_404(user_id)
    return render_template('/users/userDetails.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    '''show edit form'''
    user = User.query.get_or_404(user_id)
    return render_template('/users/userEdit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    '''process the edit form, returning the user to the /users page'''
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    new_user = User(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()
    flash(f'User {user.full_name} edited.')
    return redirect('/users')

@app.route('/users/<int:users_id>/delete', methods=["POST"])
def delete_user(user_id):
    '''Handle form submission for deleting an existing user'''
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.full_name} deleted.')
    return redirect('/users')

#################################################################################
# Posts route

@app.route('/users/<int:user_id>/posts/newpost')
def posts_new_form(user_id):
    '''show a form to create post for current user'''
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("posts/new.html", user = user, tags= tags)

@app.route('/users/<int:user_id>/posts/newpost', methods=['POST'])
def post_new(user_id):
    '''form submission for new post creation for current user'''

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title= request.form['title'],
                    content= request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def posts_display(post_id):
    '''show a post and buttons to delete and edit the post'''
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):
    """form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('/posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_update(post_id):
    """Handle form submission/ updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")

#####################################################################
# Tag route

@app.route('/tags')
def tags_index():
    '''show all tags & info '''
    tags = Tag.query.all()
    return render_template('/tags/index.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_info(tag_id):
    ''' show info on tag is '''
    info = Tag.query.get_or_404(tag_id)
    return render_template('/tags/show.html', tag=tag)

@app.route('/tags/new')
def new_tag():
    '''show form to add new tag'''
    posts = Post.query.all()
    return render_template('/tags/new.html', posts=posts)

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    '''process new form for tag '''
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit')
def show_edit_form(tag_id):
    '''show edit form for tag'''
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('/tags/edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    '''process add form, adds tag, and redirect to tag list'''
    tag = Tag.query.get_or_404(tag_id)
    tag_name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    
    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited. ")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tag_delete(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")