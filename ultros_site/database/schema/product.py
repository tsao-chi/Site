# coding=utf-8
from sqlalchemy import Column, String, Integer, Boolean, ARRAY

from ultros_site.database.common import DeclarativeBase

__author__ = "Momo"


class Product(DeclarativeBase):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    order = Column(Integer, default=1)
    hidden = Column(Boolean)

    url_github = Column(String, unique=True)
    url_circleci = Column(String, unique=True)

    branches = Column("branches", ARRAY(Integer))

    def __repr__(self):
        return "<{}(name={}>".format(
            self.__class__.__name__,
            self.name
        )