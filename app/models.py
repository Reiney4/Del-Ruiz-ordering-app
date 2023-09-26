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



