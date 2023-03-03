"""Blogly application."""

from flask import Flask, render_template, request, redirect
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug= DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def index():
    '''homepage Redirects to list of users.'''
    return redirect("/users")

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

