from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
class User(Base):
     __tablename__ = 'users'

     email = Column(String, primary_key=True)
     name = Column(String)
     Password = Column(String)

     def __repr__(self):
         return "<User(email='%s', name='%s')>" % (
                self.email, self.name)

Base.metadata.create_all(engine)
