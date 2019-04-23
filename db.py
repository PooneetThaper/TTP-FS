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
     password_hash = Column(String)
     cash = Column(Integer)

     def __repr__(self):
         return "<User(email='%s', name='%s')>" % (
                self.email, self.name)

class Holding(Base):
     __tablename__ = 'holdings'

     email = Column(String, primary_key=True)
     ticker = Column(String, primary_key=True)
     quantity = Column(String)

     def __repr__(self):
         return "<Holding(email='%s', ticker='%s', quantity='%s')>" % (
                self.email, self.name, self.quantity)

Base.metadata.create_all(engine)


def create_user(name, email, password):
    Session.add(User(
        email=email,
        name=name,
        password_hash=generate_password_hash(password),
        cash=5000))
    Session.commit()

def authenticate_user(email, password):
    user = User.query.filter(email=email)
    return check_password_hash(user.password_hash, password)
