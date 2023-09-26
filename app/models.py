# Import necessary libraries and modules

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

# create a SQLAlchemy metadata object with a custom naming convention
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# create a Flask-SQLAlchemy instance and associate it with the metadata

db = SQLAlchemy(naming_convention={})

# Define the Restaurant models
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    # Define serialization rules for the model
    serialize_rules = ('-restaurant_pizzas', 'pizzas', '-pizzas.created_at', '-pizzas.updated_at')

    # Define columns for the Restaurant table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String)
    
    # Define a relationship with Restaurant_pizzas and create an association proxy for pizzas
    restaurant_pizzas = db.relationship('Restaurant_pizzas', back_populates='restaurant', cascade='all, delete-orphan')
    pizzas = association_proxy('restaurant_pizzas', 'pizza')

    # Define a string representation for the Restaurant object
    def __repr__(self):
        return f'(id={self.id}, name={self.name} address={self.address})'
    
    # Define the Pizza model
class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    # Define serialization rules for the model
    serialize_rules = ('-restaurant_pizzas',)

    # Define columns for the Pizza table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    image = db.Column(db.String)

    # Define a relationship with Restaurant_pizzas and create an association proxy for restaurants
    restaurant_pizzas = db.relationship('Restaurant_pizzas', back_populates='pizza', cascade='all, delete-orphan')
    restaurants = association_proxy('restaurant_pizzas', 'restaurant')

    # Define a string representation for the Pizza object
    def __repr__(self):
        return f'(id={self.id}, name={self.name} ingredients={self.ingredients})'

    # Define a validator for the 'name' column
    @validates('name')
    def check_name(self, key, name):
        if len(name) > 50:
            raise ValueError("Name must be less than 50 characters")
        else:
            return name

# Define the Restaurant_pizzas model
class Restaurant_pizzas(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    # Define serialization rules for the model
    serialize_rules = ('-restaurant_pizzas', '-pizzas', '-restaurants')

    # Define columns for the Restaurant_pizzas table
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), default=0.00)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define relationships with Restaurant and Pizza and create back-references
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    # Define a string representation for the Restaurant_pizzas object
    def __repr__(self):
        return f'(id={self.id}, price={self.price} pizza={self.pizza_id} restaurant={self.restaurant_id})'

    # Define a validator for the 'price' column
    @validates('price')
    def check_price(self, key, price):
        if price not in range(1, 31):
            raise ValueError("Price must be between 1 and 30")
        else:
            return price
