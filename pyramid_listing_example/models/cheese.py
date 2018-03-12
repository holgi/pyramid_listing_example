from sqlalchemy import Column, Integer, Text

from .meta import Base

class Cheese(Base):
    ''' A cheese '''

    __tablename__ = 'cheeses'

    #: primary key
    id = Column(Integer, primary_key=True)
    #: country of origin
    country = Column(Text, nullable=False)
    #: name of the cheese
    name = Column(Text, nullable=False)
    #: region it is produced
    region = Column(Text, nullable=False)
    #: description
    description = Column(Text, nullable=False)

