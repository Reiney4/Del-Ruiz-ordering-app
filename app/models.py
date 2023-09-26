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
