import transaction
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import DateTime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Tweet(Base):
  __tablename__ = 'tweets'
  id = Column(Integer, primary_key=True)
  username = Column(Text)
  message = Column(Text)
  timestamp = Column(DateTime)
    
  def __init__(self, username, message):
    self.username = username
    self.message = message
    self.timestamp = datetime.now()

  def save(self):
    session = DBSession()
    #import pdb; pdb.set_trace()
    session.add(self)

  @staticmethod
  def get(id):
    session = DBSession()
    tweet = session.query(Tweet).filter(id=id)
    return tweet

  @staticmethod
  def delete(tweet):
    session = DBSession()
    session.delete(tweet)
    session.flush()

  @staticmethod
  def get_tweets():
    session = DBSession()
    tweets = session.query(Tweet).all()
    list = []
    for tweet in tweets:
      list.append({
        "id":tweet.id, 
        "username":tweet.username, 
        "message":tweet.message,
        "timestamp":tweet.timestamp.strftime('%x %X')})
    return list
        
def initialize_sql(engine):
  DBSession.configure(bind=engine)
  Base.metadata.bind = engine

  #This wipes out the database every time...
  Base.metadata.drop_all(engine) 

  Base.metadata.create_all(engine)
  try:
    tweet = Tweet('Kevin', 'Yet another tweet for fun')
    tweet.save()
    # Because we're not in a request, so transactions aren't autocommitted.
    transaction.commit()
  except IntegrityError:
    # already created
    pass
    
    
    