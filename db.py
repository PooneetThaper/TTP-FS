from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///foo.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
     __tablename__ = 'users'

     email = Column(String, primary_key=True)
     name = Column(String)
     password_hash = Column(String)
     cash = Column(Integer)

     def __repr__(self):
         return "<User(email='%s', name='%s', cash='%s')>" % (
                self.email, self.name, self.cash)

class Holding(Base):
     __tablename__ = 'holdings'

     email = Column(String, primary_key=True)
     ticker = Column(String, primary_key=True)
     quantity = Column(String)

     def __repr__(self):
         return "<Holding(email='%s', ticker='%s', quantity='%s')>" % (
                self.email, self.name, self.quantity)

class Transaction(Base):
     __tablename__ = 'transactions'

     email = Column(String, primary_key=True)
     date_time = Column(String, primary_key=True)
     type = Column(String)
     ticker = Column(String)
     quantity = Column(String)

     def __repr__(self):
         return "<Transaction(email='%s', date_time='%s', type='%s', ticker='%s', quantity='%s')>" % (
                self.email, self.date_time, self.type, self.name, self.quantity)

Base.metadata.create_all(engine)
session.commit()

def create_user(name, email, password):
    try:
        session.add(User(
            email=email.lower(),
            name=name,
            password_hash=generate_password_hash(password),
            cash=5000))
        session.commit()
        return True
    except:
        return False

def authenticate_user(email, password):
    user = session.query(User).filter_by(email=email.lower()).first()
    if user == None:
        return False
    return check_password_hash(user.password_hash, password)

def get_user_cash(email):
    user = session.query(User).filter_by(email=email.lower()).first()
    if user == None:
        return False
    return user.cash

def get_user_holdings(email):
    holdings = session.query(Holding).filter_by(email=email.lower()).all()
    if holdings == None:
        return False
    return holdings

def get_user_transactions(email):
    transactions = session.query(Transaction).filter_by(email=email.lower()).all()
    if transactions == None:
        return False
    return transactions
