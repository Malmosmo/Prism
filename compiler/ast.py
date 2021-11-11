from __future__ import annotations
from rply.token import BaseBox, SourcePosition, Token


class Node(BaseBox):
    def __init__(self, value: Node | str, position: SourcePosition) -> None:
        self.value = value
        self.position = position

    def rep(self) -> str:
        if isinstance(self.value, Node):
            return f"{self.__class__.__name__}({self.value.rep()})"

        else:
            return f"{self.__class__.__name__}({self.value})"

    def getsourcepos(self) -> SourcePosition:
        return self.position

    def generate(self) -> str:
        pass


##################################################
# Program
##################################################
class ProgramNode(Node):
    def generate(self) -> str:
        return f"package main\n\n{self.value.generate()}"


##################################################
# Functions
##################################################
class FuncNode(Node):
    def __init__(self, type_: str, name: str, body: Node, return_value: Node, position: SourcePosition) -> None:
        self.type = type_
        self.name = name
        self.body = body
        self.return_value = return_value
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.type.rep()}, {self.name}, {self.body.rep()}, {self.return_value.rep()})"

    def generate(self) -> str:
        return f"func {self.name} () {self.type} {{\n{self.body.generate()}\n{self.return_value.generate()}\n}}"


class VoidFuncNode(Node):
    def __init__(self, name: str, body: Node, position: SourcePosition) -> None:
        self.name = name
        self.body = body
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.body.rep()})"

    def generate(self) -> str:
        return f"func {self.name} () {{\n{self.body.generate()}\n}}"


##################################################
# Builtin Functions
##################################################
class BuiltinFunctionNode(Node):
    def __init__(self, func: str, value: Node, position: SourcePosition) -> None:
        self.func = func
        super().__init__(value, position)

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.func}, {self.value.rep()})"

    def generate(self) -> str:
        return f"{self.func}({self.value.generate()})"


##################################################
# Return
##################################################
class ReturnNode(Node):
    def generate(self) -> str:
        return f"return {self.value.generate()}"


##################################################
# Block
##################################################
class BlockNode(Node):
    def __init__(self, value: Node, position: SourcePosition) -> None:
        self.commands = [value]
        self.position = position

    def add(self, value: Node) -> None:
        self.commands.append(value)

    def rep(self) -> str:
        return f"{self.__class__.__name__}([{', '.join((command.rep() for command in self.commands))}])"

    def generate(self) -> str:
        return "\n".join(command.generate() for command in self.commands)


##################################################
# Binary Operations
##################################################
class BinaryOpNode(Node):
    def __init__(self, operand: str, left: Node, right: Node, position: SourcePosition) -> None:
        self.operand = operand
        self.left = left
        self.right = right
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.left.rep()} {self.operand} {self.right.rep()})"

    def generate(self) -> str:
        return f"({self.left.generate()} {self.operand} {self.right.generate()})"


##################################################
# Variables
##################################################
class VarDecNode(Node):
    def __init__(self, type_: Node, name: str, value: Node, position: SourcePosition) -> None:
        self.type = type_
        self.name = name
        super().__init__(value, position)

    def rep(self):
        return f"{self.__class__.__name__}({self.type.rep()}, {self.name}, {self.value.rep()})"

    def generate(self) -> str:
        return f"var {self.name} {self.type.generate()} = {self.value.generate()}"


class VarAssignNode(Node):
    def __init__(self, name: str, value: Node, position: SourcePosition) -> None:
        self.name = name
        super().__init__(value, position)

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.value.rep()})"

    def generate(self) -> str:
        return f"{self.name} = {self.value.generate()}"


class VarAccessNode(Node):
    def __init__(self, value: str, position: SourcePosition) -> None:
        self.value = value
        self.position = position

    def generate(self) -> str:
        return self.value


##################################################
# Types
##################################################
class TypeNode(Node):
    def __init__(self, value: str, position: SourcePosition) -> None:
        self.value = value
        self.position = position

    def generate(self) -> str:
        return self.value

##################################################
# Expressions
##################################################


##################################################
# Literals
##################################################
class IntegerNode(Node):
    def __init__(self, value: str, position: SourcePosition) -> None:
        self.value = value
        self.position = position

    def generate(self) -> str:
        return self.value


class StringNode(Node):
    def generate(self) -> str:
        return self.value
