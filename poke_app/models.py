from werkzeug.security import generate_password_hash #generates a unique password hash for extra security 
from flask_sqlalchemy import SQLAlchemy #this is our ORM (Object Relational Mapper)
from flask_login import UserMixin, LoginManager #helping us load a user as our current_user 
from datetime import datetime #put a timestamp on any data we create (Users, Products, etc)
import uuid #makes a unique id for our data (primary key)
from flask_marshmallow import Marshmallow



#instantiate all our classes
db = SQLAlchemy() #make database object
login_manager = LoginManager() #makes login object 
ma = Marshmallow() #makes marshmallow object


#use login_manager object to create a user_loader function
@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id) #this is a basic query inside our database to bring back a specific User object

#think of these as admin (keeping track of what products are available to sell)
class User(db.Model, UserMixin): 
    #CREATE TABLE User, all the columns we create
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow) #this is going to grab a timestamp as soon as a User object is instantiated


    #INSERT INTO User() Values()
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email 
        self.password = self.set_password(password) 



    #methods for editting our attributes 
    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token
    

    def get_id(self):
        return str(self.user_id) #UserMixin using this method to grab the user_id on the object logged in
    
    
    def set_password(self, password):
        return generate_password_hash(password) #hashes the password so it is secure (aka no one can see it)
    

    def __repr__(self):
        return f"<User: {self.username}>"
    
    pokemons = db.relationship('Pokemon', backref='trainer', lazy='dynamic')

class Pokemon(db.Model):
    poke_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    pokemon_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255))  # URL to the image
    description = db.Column(db.String(200))
    type = db.Column(db.String(50), nullable=False)
    abilities = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'))


    def __repr__(self):
        return f"<Pokemon: {self.pokemon_name}>"

class PokemonSchema(ma.Schema):
    class Meta:
        fields = ['poke_id', 'pokemon_name', 'image_url', 'description', 'type', 'abilities']

# Instantiate our PokemonSchema class so we can use them in our application
pokemon_schema = PokemonSchema()  # For serializing a single Pokemon
pokemons_schema = PokemonSchema(many=True)  # For serializing multiple Pokemon