from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, InvalidRequestError

class Database():
    Base = declarative_base()
    def __init__(self, dblocation):
        self.engine = create_engine('sqlite:///' + dblocation, convert_unicode = True)
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=self.engine))
        self.Base.query = self.session.query_property()
        self.Base.metadata.create_all(bind = self.engine)

class Comment(Database.Base):
    __tablename__ = 'comments'
    id = Column(String, primary_key=True)

    def __init__(self, comment_id):
        self.id = comment_id

    @staticmethod
    def add(id, session):
        try:
            session.merge(Comment(id))
            session.commit()
        except (IntegrityError, InvalidRequestError):
            pass
        except:
            raise

    @staticmethod
    def is_parsed(id):
        return Comment.query.filter(Comment.id == id).count() > 0

class Submission(Database.Base):
    __tablename__ = 'submissions'
    id = Column(String, primary_key=True)

    def __init__(self, submission_id):
        self.id = submission_id

    @staticmethod
    def add(id, session):
        try:
            session.merge(Submission(id))
            session.commit()
        except (IntegrityError, InvalidRequestError):
            pass
        except:
            raise

    @staticmethod
    def is_parsed(id):
        return Submission.query.filter(Submission.id == id).count() > 0
