from __future__ import annotations
import hashlib
from rply.token import BaseBox, SourcePosition


__HASH__ = "12345678"


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


class BlockNode(Node):
    def __init__(self, value: Node | str, position: SourcePosition) -> None:
        self.statements = [value]
        self.position = position

    def add(self, value: Node):
        self.statements.append(value)

    def rep(self) -> str:
        return f"{self.__class__.__name__}([{''.join(stmt.rep() for stmt in self.statements)}])"

    def generate(self) -> str:
        return "\n".join(stmt.generate() for stmt in self.statements)


class ListNode(BlockNode):
    def __init__(self, value: Node | str, separator: str, position: SourcePosition) -> None:
        self.statements = [value]
        self.separator = separator
        self.position = position

    def generate(self) -> str:
        return self.separator.join(stmt.generate() for stmt in self.statements)


class ProgrammNode(Node):
    def __init__(self, value: Node | str, position: SourcePosition) -> None:
        super().__init__(value, position)

    def generate(self) -> str:
        return f"programm"


##################################################
# Class
##################################################
class ClassNode(Node):
    def __init__(self, name: str, body: Node, position: SourcePosition) -> None:
        self.name = name
        self.body = body
        self.position = position

    def generate(self) -> str:
        return f"type {self.name} struct {{ {self.body.generate_attributes()} }} \n" + self.body.generate(self.name)


class ClassCompoundNode(Node):
    def __init__(self, attributes: Node, methods: Node, position: SourcePosition) -> None:
        self.attributes = attributes
        self.methods = methods
        self.position = position

    def generate_attributes(self) -> str:
        if self.attributes:
            return "\n".join([attr.generate() for attr in self.attributes.statements])

        return ""

    def generate_methods(self, class_name: str) -> str:
        if self.methods:
            return "\n".join([method.generate_as_method(class_name) for method in self.methods.statements])

        return ""

    def generate(self, class_name: str = "") -> str:
        return self.generate_methods(class_name)


##################################################
# Constant
##################################################
class ConstantNode(Node):
    def __init__(self, _type: Node, decl: Node, initalizer: Node, position: SourcePosition) -> None:
        self._type = _type
        self.decl = decl
        self.initalizer = initalizer
        self.position = position

    def generate(self) -> str:
        return f"const {self.decl.generate()} {self._type.generate()} = {self.initalizer.generate()}"


##################################################
# Function
##################################################
class FunctionDeclarationNode(Node):
    def __init__(self, name: str, parameter: Node | None, position: SourcePosition) -> None:
        self.name = name
        self.parameter = parameter
        self.position = position

    def generate(self) -> str:
        return f"{self.name}({self.parameter.generate()})"

    def generate_as_method(self, class_name: str) -> str:
        global __HASH__

        signature = f"(this {class_name}, {self.parameter.generate()})"
        _hash = hashlib.sha1((signature + __HASH__).encode()).hexdigest()[:8]
        __HASH__ = _hash

        return f"{self.name}__{class_name}__{_hash}{signature}"


class FunctionSignatureNode(Node):
    def __init__(self, decl: Node, return_type: Node, position: SourcePosition) -> None:
        self.decl = decl
        self.return_type = return_type
        self.position = position

    def generate(self) -> str:
        return f"{self.decl.generate()} {self.return_type.generate()}"

    def generate_as_method(self, class_name: str) -> str:
        return f"{self.decl.generate_as_method(class_name)} {self.return_type.generate()}"


class FunctionNode(Node):
    def __init__(self, signature: Node, body: Node, position: SourcePosition) -> None:
        self.signature = signature
        self.body = body
        self.position = position

    def generate(self) -> str:
        return f"func {self.signature.generate()} {self.body.generate()}"

    def generate_as_method(self, class_name: str) -> str:
        return f"func {self.signature.generate_as_method(class_name)} {self.body.generate()}"


class ParameterNode(Node):
    def __init__(self, _type: Node, declarator: Node, position: SourcePosition) -> None:
        self._type = _type
        self.declarator = declarator
        self.position = position

    def generate(self) -> str:
        return f"{self.declarator.generate()} {self._type.generate()}"


##################################################
# Statement
##################################################
class CompoundNode(Node):
    def __init__(self, value: Node, position: SourcePosition) -> None:
        super().__init__(value, position)

    def generate(self) -> str:
        return "{\n" + self.value.generate() + "\n}"


class JumpNode(Node):
    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.value.rep()})"

    def generate(self) -> str:
        return f"return {self.value.generate()}"


class IfNode(Node):
    def __init__(self, condition: Node, body: Node, position: SourcePosition) -> None:
        self.condition = condition
        self.body = body
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.condition.rep()} {self.body.rep()})"

    def generate(self) -> str:
        return f"if ({self.condition.generate()}) {self.body.generate()}"


class IfElseNode(Node):
    def __init__(self, condition: Node, body: Node, else_body: Node, position: SourcePosition) -> None:
        self.condition = condition
        self.body = body
        self.else_body = else_body
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.condition.rep()} {self.body.rep()} {self.else_body.rep()})"

    def generate(self) -> str:
        return f"if ({self.condition.generate()}) {self.body.generate()} else {self.else_body.generate()}"


class WhileNode(Node):
    def __init__(self, condition: Node, body: Node, position: SourcePosition) -> None:
        self.condition = condition
        self.body = body
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.condition.rep()} {self.body.rep()})"

    def generate(self) -> str:
        return f"for ({self.condition.generate()}) {self.body.generate()}"


class ForNode(Node):
    def __init__(self, decl: Node, expr_1: Node, expr_2: Node, body: Node, position: SourcePosition) -> None:
        self.decl = decl
        self.expr_1 = expr_1
        self.expr_2 = expr_2
        self.body = body
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.decl.rep()} {self.body.rep()})"

    def generate(self) -> str:
        return f"for {self.decl.implicit()} ; {self.expr_1.generate()} ; {self.expr_2.generate()} {self.body.generate()}"


# class FunctionNode(Node):
#     def __init__(self, name: str, decl: Node, position: SourcePosition) -> None:
#         self.name = name
#         self.decl = decl
#         self.position = position

#     def rep(self) -> str:
#         return f"{self.__class__.__name__}()"

#     def generate(self) -> str:
#         return f"func {self.name} {self.decl.generate()}"


class CallNode(Node):
    def __init__(self, func: Node, args: Node, position: SourcePosition) -> None:
        self.func = func
        self.args = args
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.func.rep()} {self.args.rep()})"

    def generate(self) -> str:
        return f"{self.func.generate()}({self.args.generate()})"


##################################################
# Declaration
##################################################
class DeclarationNode(Node):
    def __init__(self, _type: Node, value: Node | str, position: SourcePosition) -> None:
        self._type = _type
        self.value = value
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self._type.rep()} {self.value.rep()})"

    def generate(self) -> str:
        return f"var {self.value.generate()} {self._type.generate()}"


class DeclarationAssgnNode(Node):
    def __init__(self, _type: Node, declarator: Node, initalizer: Node, position: SourcePosition) -> None:
        self._type = _type
        self.declarator = declarator
        self.initalizer = initalizer
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self._type.rep()} {self.declarator.rep()} = {self.initalizer.rep()})"

    def generate(self) -> str:
        return f"var {self.declarator.generate()} {self._type.generate()} = {self.initalizer.generate()}"

    def implicit(self) -> str:
        return f"{self.declarator.generate()} := {self.initalizer.generate()}"


class PointerNode(Node):
    def __init__(self, pointer: str, value: Node, position: SourcePosition) -> None:
        self.pointer = pointer
        super().__init__(value, position)

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.pointer} {self.value.rep()})"

    def generate(self) -> str:
        return f"{self.pointer} {self.value.generate()}"


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
        return f"{self.left.generate()} {self.operand} {self.right.generate()}"


##################################################
# Unary Operations
##################################################
class UnaryOpNode(Node):
    def __init__(self, operand: str, value: Node, position: SourcePosition) -> None:
        self.operand = operand
        self.value = value
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.operand} {self.value.rep()})"

    def generate(self) -> str:
        return f"{self.operand} {self.value.generate()}"


##################################################
# Cast Operations
##################################################
class CastNode(Node):
    def __init__(self, _type: Node, value: Node, position: SourcePosition) -> None:
        self._type = _type
        self.value = value
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self._type.rep()} {self.value.rep()})"

    def generate(self) -> str:
        return f"({self._type.generate()}){self.value.generate()}"


class TypeNode(Node):
    def __init__(self, value: str, position: SourcePosition) -> None:
        super().__init__(value, position)

    def generate(self) -> str:
        return self.value


class IncrementNode(Node):
    def __init__(self, value: Node, position: SourcePosition) -> None:
        super().__init__(value, position)

    def generate(self) -> str:
        return f"{self.value.generate()} ++"


class MemberAccessNode(Node):
    def __init__(self, obj: Node, member: Node, position: SourcePosition) -> None:
        self.obj = obj
        self.member = member
        self.position = position

    def rep(self) -> str:
        return f"{self.__class__.__name__}({self.obj.rep()} {self.member.rep()})"

    def generate(self) -> str:
        return f"{self.obj.generate()}.{self.member.generate()}"


##################################################
# !!
##################################################
class ValueNode(Node):
    def __init__(self, _type: str, value: str, position: SourcePosition) -> None:
        self._type = _type
        self.value = value
        self.position = position

    def rep(self) -> str:
        return f"Value:{self._type}->{self.value}"

    def generate(self) -> str:
        return self.value


class EmptyNode(Node):
    def __init__(self) -> None:
        pass

    def generate(self) -> str:
        return ""
