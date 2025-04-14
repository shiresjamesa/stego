"""Database.py
"""
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import MetaData, inspect
from sqlalchemy import Column, Integer, String, Float, LargeBinary
from sqlalchemy import PickleType, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from util.Question import Question, Board
from util.User import User
import hashlib
from util.Status import Status
import os

Base = declarative_base()

class QuestionTable(Base):
    # TODO: Add support for multimedia questions
    """Class to provide DB model for a Trivial Compute Question.

    Attributes:
        id (int): Question ID
        category (str): Question Category
        data (str): Textual Question
        answer (str): Text Answer to Question
    """
    __tablename__ = "Questions"

    id = Column(String, primary_key=True) # question id
    board_id = Column(String, ForeignKey("Boards.id"))
    category = Column(String)
    data = Column(String) # question string
    hasMultChoice = Column(Boolean)
    multChoiceA = Column(String)
    multChoiceB = Column(String)
    multChoiceC = Column(String)
    multChoiceD = Column(String)
    hasMultimedia = Column(Boolean)
    multimedia = Column(String) # multimedia data (string for now)
    answer = Column(String)

    # relationship
    board_rel = relationship("BoardTable")


class BoardTable(Base):
    """Class to provide DB model for a Trivial Compute Board.

    Attributes:
        id (int): ID of the board
        title (str): Title of the board
        author (str): Author of the board
        description (str): Description of the board
        categories (list[str]): List of 4 categories that belong to the board
    """
    __tablename__ = "Boards"

    id = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    categories = Column(PickleType)


class UserTable(Base):
    __tablename__ = "Users"
    
    
    # Columns
    # id's
    id = Column(Integer, primary_key=True)
    
    # Parameters
    username = Column(String)
    password = Column(String)
    email = Column(String)
    
    # Initialize Schema
    def __init__(self, user:User):
        self.username = user.username
        self.email = user.email
        self.password = user.password


class MultimediaTable(Base):
    """Class to provide DB model for multimedia.

    Attributes:
        id (int): ID of the multimedia
        question_id (str): question_id
        filepath (str): filepath to the multimedia stored on disc
    """

    __tablename__ = "Multimedia"

    # Columns
    # id's
    id = Column(Integer, primary_key=True)
    question_id = Column(String, ForeignKey("Questions.id"))
    
    # Parameters
    filename = Column(String)
    blob = Column(LargeBinary)
    
    # Initialize Schema
    def __init__(self, question_id:str, filename:str, blob:bytes):
        self.question_id = question_id
        self.filename = filename
        self.blob = blob


class Database:
    """Class to initialize the question database.

    Attributes:
        engine
        Session
    """
    def __init__(self, url):
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


    def add_board(self, board: Board, questions:list[Question]):
        '''Function to add an entire board to database
        a board has 4 categories and a variety of questions within each category
        '''

        # open DB session
        session = self.Session()

        try:
            if not self.board_exists(board):
                # add board
                board_model = BoardTable(
                    id=board.id,
                    title=board.title,
                    author=board.author,
                    description=board.desc,
                    categories = board.categories)
                session.add(board_model)
                session.commit()

                # get board_id
                board_id = board_model.id

                # add questions
                for question in questions:
                    question_model = QuestionTable(
                        id=question.id,
                        board_id=board_id,
                        category=question.category,
                        data=question.data,
                        answer=question.answer,
                        hasMultChoice=question.hasMultChoice,
                        multChoiceA=question.multChoiceA,
                        multChoiceB=question.multChoiceB,
                        multChoiceC=question.multChoiceC,
                        multChoiceD=question.multChoiceD,
                        hasMultimedia=question.hasMultimedia,
                        multimedia=question.multimedia)
                    
                    if not self.question_exists(question):
                        session.add(question_model)

                # leave commit outside of loop, else we may lock the database and get overwrite error
                session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()


    def delete_board(self, board_id:str):
        """Function to delete a board
        
        @param board_id (str): id of the board to be deleted
        """

        session = self.Session()

        # query all questions that match the board_id
        questions = session.query(QuestionTable)\
            .filter(QuestionTable.board_id==board_id).all()
        
        # delete each question from database
        for question in questions:
            session.delete(question)

            # remove multimedia if any
            multimedia = session.query(MultimediaTable)\
                                .filter(MultimediaTable.question_id==question.id).first()
            
            session.delete(multimedia)

        session.commit()

        # now, remove board from table
        board = session.query(BoardTable).filter(BoardTable.id==board_id).first()
        session.delete(board)

        session.commit()
        session.close()


    def get_boards(self) -> dict[BoardTable,dict[str,list[QuestionTable]]]:
        """Function to get all boards from the database

        @returns: dict{BoardTable: dict{category: Question}}
        """
        # open DB session
        session = self.Session()

        # initialize dict
        board_dict = {}

        board_qeuery = session.query(BoardTable).all()

        # for each board, add questions to the dictionary that associate with that board
        for board in board_qeuery:
            board_dict[board] = {}

            # for each category within that board
            for category in board.categories:
                board_dict[board][category] = []
                

                # filter questions that tie to that board id and category
                questions = session.query(QuestionTable)\
                    .filter(QuestionTable.board_id==board.id)\
                    .filter(QuestionTable.category==category)\
                    .all()

                for question in questions:
                    board_dict[board][category].append(question)

        session.close()

        return board_dict



# TODO I updated the name of this method, need to update whereever this is called. Actually we can delete this
    def add_question(self, question):
        """Function to add question to database.
        """
        # open DB session
        session = self.Session()

        try:
            if not self.question_exists(question):
                question_model = QuestionTable(
                    id=question.id,
                    category=question.category,
                    data=question.data,
                    answer=question.answer)
                session.add(question_model)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def question_exists(self, question):
        """Function to check if question already exists in DB.
        """
        session = self.Session()
        try:
            return session.query(QuestionTable).filter_by(id=question.getId()).first() is not None
        finally:
            session.close()

    def board_exists(self, board: Board) -> bool:
        """Function to check if board already exists in DB.
        """
        session = self.Session()
        try:
            return session.query(BoardTable).filter_by(id=board.getId()).first() is not None
        finally:
            session.close()
    

    def add_user(self, user:User) -> Status:
        # connect to database
        session = self.Session()
        
        
        # check if user already exists in database
        user_exists = True if self.get_user(user.username) else False
        email_exists = self.email_exists(user.email)
        
        # if username already exists in the database, return False
        if user_exists:
            return Status(False, "Username already in use")

        # if email already exists in database, return False
        elif email_exists:
            return Status(False, "Email already in use")
        
        # if both username and email are available, make new user
        else:
            new_user = UserTable(user)
            session.add(new_user)
        
            # commit
            session.commit()

        # close session
        session.close()

        # return status
        return Status(True, "user successfully registered")
    

    def get_user(self, username:str):
        """Function to check if username already exists in DB.

        @param username (str): username
        """
        session = self.Session()
        try:
            return session.query(UserTable).filter(UserTable.username==username).first()
        finally:
            session.close()

    def get_board(self, board_id:int):
       """Function to retrieve Board object from DB

       @param board_id (int): Board ID

       """
       session = self.Session()
       try:
           return session.query(BoardTable).filter(BoardTable.id==board_id).first()
       finally:
           session.close()


    def add_multimedia(self, question_id:str, filename:str, blob:bytes):
        """Function to add multimedia filepath to database

        @param question_id (str): Question ID
        @param filepath (str): filepath to where the file is stored
        """
        session = self.Session()

        # check if multimedia already exists in table
        exists = True if self.multimedia_exists(question_id) else False
        
        # if multimedia already exists for question, the replace it
        if exists:
            multimedia = self.get_multimedia(question_id)
            multimedia.filename = filename
            multimedia.blob = blob
        
        # if doesn't already exist, add to database
        else:
            new_entry = MultimediaTable(question_id, filename, blob)
            session.add(new_entry)
        
        # commit
        session.commit()

        # close session
        session.close()

        # return status
        return Status(True, "multimedia added")


    def get_multimedia(self, question_id:str):
        """Function to get multimedia filepath from database

        @param question_id (str): Question ID
        """
        session = self.Session()
        try:
            return session.query(MultimediaTable)\
                .filter(MultimediaTable.question_id==question_id)\
                .first()
        
        except:
            return None
        
        finally:
            session.close()            


    def multimedia_exists(self, question_id:str):
        """Function to see if multimedia exists in database

        @param question_id (str): Question ID
        """
        session = self.Session()
        try:
            return session.query(MultimediaTable)\
                .filter(MultimediaTable.question_id==question_id)\
                .first() is not None
        finally:
            session.close()       


    def email_exists(self, email:str):
        """Function to check if email already exists in DB.
        """
        session = self.Session()
        try:
            return session.query(UserTable).filter(UserTable.email==email).first() is not None
        finally:
            session.close()
    

    def loginRequest(self, username:str, password:str) -> Status:
        # hash the password
        password = str(hashlib.sha256(bytes(password, "utf-8")).hexdigest())


        # grab the user from the database
        user = self.get_user(username)

        # if username does not exist, return False
        if (not user):
            return Status(False, "username does not exist")

        # if password is incorrect, return False
        elif user.password != password:
            return Status(False, "password is incorrect")
            
        # else, login is successful!
        else:
            return Status(True, "successfully logged in")
