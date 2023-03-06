"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()


# MODELS BELOW:
class User(db.Model):
    '''user of site'''

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key= True,
                    autoincrement=True)
    
    first_name = db.Column(db.String(25),
                        nullable=False)

    last_name = db.Column(db.String(25),
                        nullable=False)
    
    image_url = db.Column(db.String(200), 
                        nullable=True)
    
    posts = db.relatioinship("Post", backref='user', cascade='all, delete-orphan')
    @property
    def full_name(self):
        '''Return full name of user.'''

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    ''' Blog post '''
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement= True)
    
    title = db.Column(db.Text, 
                      nullable= False)

    content = db.Column(db.Text, 
                      nullable= False)

    created_at = db.Column(db.DateTime,
                            nullable=False,
                            defalut= datetime.datetime.now)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable= False)
    @property
    def nice_date(self):
        '''return formatted date looks nice'''
        return self.created_at.strftime('%a %b %-d %Y, %-I:%M %p')

        
def connect_db(app):
    ''' called in app.py, helps connect to database'''
    
    db.app = app
    db.init_app(app)


