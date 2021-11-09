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
    def __init__(self, type_, name, body, return_value, position: SourcePosition) -> None:
        self.type = type_
        self.name = name
        self.body = body
        self.return_value = return_value
        self.position = position

    def rep(self):
        return f"{self.__class__.__name__}({self.type.rep()}, {self.name}, {self.body.rep()}, {self.return_value.rep()})"


class VoidFuncNode(Node):
    def __init__(self, name, body, position: SourcePosition) -> None:
        self.name = name
        self.body = body
        self.position = position

    def rep(self):
        return f"{self.__class__.__name__}({self.name}, {self.body.rep()})"


##################################################
# Builtin Functions
##################################################
class BuiltinFunctionNode(Node):
    def __init__(self, func, value, position: SourcePosition) -> None:
        self.func = func
        self.value = value
        self.position = position

    def rep(self):
        return f"{self.__class__.__name__}({self.func}, {self.value.rep()})"


##################################################
# Return
##################################################
class ReturnNode(Node):
    def __init__(self, value, position: SourcePosition) -> None:
        super().__init__(value, position)


##################################################
# Block
##################################################
class BlockNode(Node):
    def __init__(self, value, position: SourcePosition) -> None:
        self.commands = value
        self.position = position

    def add(self, value):
        self.commands.append(value)

    def rep(self):
        return f"{self.__class__.__name__}([{', '.join((command.rep() for command in self.commands))}])"


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
# Types
##################################################
class TypeNode(Node):
    pass


##################################################
# Expressions
##################################################
class IntegerNode(Node):
    def rep(self):
        return f"{self.__class__.__name__}({self.value})"
