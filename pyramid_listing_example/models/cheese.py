from sqlalchemy import Column, Integer, Unicode

from .meta import Base


class Cheese(Base):
    ''' A cheese '''

    __tablename__ = 'cheeses'

    #: primary key
    id = Column(Integer, primary_key=True)
    #: country of origin
    country = Column(Unicode, nullable=False)
    #: name of the cheese
    name = Column(Unicode, nullable=False)
    #: region it is produced
    region = Column(Unicode, nullable=False)
    #: description
    description = Column(Unicode, nullable=False)

