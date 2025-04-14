"""Question.py
"""
class Question:
    """Class to model a Trivial Compute Question.

    Attributes:
        id (int): Unique identifier for the Question.
        data (Data): Question data (textual / multimedia)
        answer (str): Answer to the question
        category (str): Category which the question belongs to
    """
    def __init__(self, id:str, data, answer:str, category:str, hasMultChoice:bool=False,
                 multChoiceA:str=None, multChoiceB:str=None, multChoiceC:str=None, multChoiceD:str=None,
                 hasMultimedia:bool=False, multimedia:str=None):
        self.id = id
        self.data = data
        self.answer = answer
        self.category = category
        self.hasMultChoice = hasMultChoice
        self.multChoiceA = multChoiceA
        self.multChoiceB = multChoiceB
        self.multChoiceC = multChoiceC
        self.multChoiceD = multChoiceD
        self.hasMultimedia = hasMultimedia
        self.multimedia = multimedia

    def setId(self, id:str):
        self.id = id

    def getId(self)->str:
        return self.id

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def setAnswer(self, answer:str):
        self.answer = answer

    def getAnswer(self)->str:
        return self.answer

    def setCategory(self, category:str):
        self.category = category

    def getCategory(self)->str:
        return self.category
    
    # TODO add getters and setters for new attributes
    


class Board:
    """Class to model a Trivial Compute Board.

    Attributes:
        id (int): Unique identifier for the Question.
        data (Data): Question data (textual / multimedia)
        answer (str): Answer to the question
        category (str): Category which the question belongs to
        """
    
    def __init__(self, id: str, title: str, author: str, desc: str, categories: list[str]) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.desc = desc
        self.categories = categories

    def setId(self, id:str):
        self.id = id

    def getId(self)->str:
        return self.id

    def setTitle(self, title:str):
        self.title = title

    def getTitle(self)->str:
        return self.title

    def setAuthor(self, author:str):
        self.author = author

    def getAuthor(self)->str:
        return self.author

    def setDesc(self, desc:str):
        self.desc = desc

    def getDesc(self)->str:
        return self.desc

    def setCategories(self, categories:list):
        self.categories = categories

    def getCategories(self)->list:
        return self.categories

