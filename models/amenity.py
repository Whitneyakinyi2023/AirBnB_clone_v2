#!/usr/bin/python3
""" Updatesd amenities module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String
from sqlalchemy import relationship


class Amenity(BaseModel, Base):
    """Amenities in MySQL"""
    __tablename__ = "amenities"
    id = Column(String(60), primary_key=True)
    name = Column(String(128), nullable=False)

    place_amenities = relationship(
        "Place", secondary="place_amenity", viewonly=False
    )
