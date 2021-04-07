from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings


Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class Suspension(Base):
    def __init__(self, id=None, title=None, description=None, price=None, balance=None, producer=None, model_auto=None, image=None, product_url = None, image_alt=None, imageurl=None):
        self.id = id
        self.title = title
        self.price = price
        self.balance = balance
        self.description = description
        self.producer = producer
        self.model_auto = model_auto
        self.image = image
        self.image_alt = image_alt
        self.product_url = product_url
        self.image_url = imageurl


    __tablename__ = "suspension"

    id = Column(Integer, primary_key=True)
    title = Column('title', Text())
    price = Column('price', Text())
    balance = Column('balance', Text())
    description = Column('description', Text())
    producer = Column('producer', Text())
    model_auto = Column('model_auto', Text())
    image = Column('image', Text())
    image_alt = Column('image_alt', Text())
    product_url = Column('product_url', Text())

