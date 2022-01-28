from sqlalchemy import Column,ForeignKey, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Facs(Base):
    __tablename__ = 'Faculties'
    id = Column(Integer,nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True)
    fac_id = Column(String(255))
    fac_name = Column(String(255))

    def __repr__(self):
        return f'{self.id} {self.fac_id} {self.fac_name}'


class Groups(Base):
    __tablename__='Groups'
    id = Column(Integer,nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True)
    group_name = Column(String(255))
    fac_id = Column(Integer,  ForeignKey(Facs.id))
    facs = relationship('Facs', backref='quote_fac', lazy='subquery' )

    def __repr__(self):
        return f'{self.id} {self.group_mame} {self.fac_id}'

class Lessons(Base):
    __tablename__ = 'Lessons'
    id = Column(Integer,nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True)
    time = Column(Time)
    room = Column(String(255))
    tittle = Column(String(255))
    tut_name = Column(String(255))
    day = Column(String(255))
    week = Column(Integer)
    group_id = Column(Integer,  ForeignKey(Groups.id))
    group = relationship('Groups', backref='quote_group', lazy='subquery')

    def __repr__(self):
        return f'{self.id} {self.time}{self.room} {self.group_id} {self.tittle}{self.tut_name}{self.day}{self.week}'