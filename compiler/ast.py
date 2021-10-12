from __future__ import annotations
from rply.token import BaseBox, SourcePosition, Token


class Node(BaseBox):
    def __init__(self, value, position: SourcePosition) -> None:
        self.value = value
        self.position = position

    def rep(self):
        return f"{self.__class__.__name__}({self.value.rep()})"

    def getsourcepos(self):
        return self.position


class ProgramNode(Node):
    pass


##################################################
# Functions
##################################################
class FuncNode(Node):
    def __init__(self, type_, name, body, position: SourcePosition) -> None:
        self.type = type_
        self.name = name
        self.body = body
        self.position = position

    def rep(self):
        return f"{self.__class__.__name__}({self.type.rep()}, {self.name}, {self.body.rep()})"


##################################################
# Types
##################################################
class TypeIntNode(Node):
    def rep(self):
        return f"{self.__class__.__name__}({self.value})"


##################################################
# Expressions
##################################################
class AssignNode(Node):
    def __init__(self, name, value, position: SourcePosition) -> None:
        self.name = name
        super().__init__(value, position)

    def rep(self):
        return f"{self.__class__.__name__}({self.name}, {self.value.rep()})"


##################################################
# Expressions
##################################################
class IntegerNode(Node):
    def rep(self):
        return f"{self.__class__.__name__}({self.value})"
