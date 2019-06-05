from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from datetime import datetime

engine = create_engine('sqlite:///foo.db', echo=True)
session = scoped_session(sessionmaker(bind=engine))
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
     quantity = Column(Integer)

     def __repr__(self):
         return "<Holding(email='%s', ticker='%s', quantity='%s')>" % (
                self.email, self.ticker, self.quantity)

class Transaction(Base):
     __tablename__ = 'transactions'

     email = Column(String, primary_key=True)
     date_time = Column(String, primary_key=True)
     type = Column(String)
     ticker = Column(String)
     quantity = Column(Integer)
     amount = Column(String)

     def __repr__(self):
         return "<Transaction(email='%s', date_time='%s', type='%s', ticker='%s', quantity='%s', amount='%s')>" % (
                self.email, self.date_time, self.type, self.ticker, self.quantity, self.amount)

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

def create_transaction(email, type, ticker, quantity, amount):
    try:
        session.add(Transaction(
            email=email.lower(),
            date_time=datetime.now(),
            type=type,
            ticker=ticker,
            quantity=quantity,
            amount=amount))
        session.commit()
        return True
    except:
        return False

def get_user_cash(email):
    user = session.query(User).filter_by(email=email.lower()).first()
    if user == None:
        return False
    retval = user.cash
    user = None
    return retval

def get_user_holdings(email, ticker=None):
    if ticker:
        holding = session.query(Holding).filter_by(email=email.lower()).filter_by(ticker=ticker).first()
        return holding
    else:
        holdings = session.query(Holding).filter_by(email=email.lower()).all()
        return holdings

def get_user_transactions(email):
    transactions = session.query(Transaction).filter_by(email=email.lower()).all()
    return transactions

def update_user_cash(email, new_value):
    user = session.query(User).filter_by(email=email.lower()).first()
    if user == None:
        return False
    user.cash = new_value
    session.commit()
    return True

def update_holding(email, ticker, quantity):
    holding = get_user_holdings(email, ticker=ticker)
    if holding == None:
        try:
            session.add(Holding(
                email=email.lower(),
                ticker=ticker,
                quantity=quantity))
            session.commit()
            return True
        except:
            return False
    else:
        holding.quantity += quantity
        if holding.quantity == 0:
            session.delete(holding)
        session.commit()
        return True
