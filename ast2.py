from __future__ import annotations
from rply.token import BaseBox, SourcePosition


class Node(BaseBox):
    def __init__(self, value: Node | str, position: SourcePosition) -> None:
        self.value = value
        self.position = position

    def getsourcepos(self) -> SourcePosition:
        return self.position

    def clang(self) -> str:
        pass


class EmptyNode(Node):
    def __init__(self) -> None:
        pass

    def clang(self) -> str:
        return ""


class BlockNode(Node):
    def __init__(self, value: Node, position: SourcePosition) -> None:
        self.statements = [value]
        self.position = position

    def add(self, value: Node):
        self.statements.append(value)

    def clang(self) -> str:
        return "\n".join(statement.clang() for statement in self.statements)


class ListNode(Node):
    def __init__(self, value: Node | str, separator: str, position: SourcePosition) -> None:
        self.separator = separator
        self._list = [value]
        self.position = position

    def add(self, value: Node | str):
        self._list.append(value)

    def clang(self) -> str:
        return self.separator.join(element.clang() for element in self._list)


# ==================================================================================================
# ==================================================================================================
# ==================================================================================================

class FunctionNode(Node):
    def __init__(self, signature: Node, body: Node, position: SourcePosition) -> None:
        self.signature = signature
        self.body = body
        self.position = position

    def clang(self) -> str:
        return f"{self.signature.clang()} {self.body.clang()}"


class FunctionSignatureNode(Node):
    def __init__(self, decl: Node, _type: Node, position: SourcePosition) -> None:
        self.decl = decl
        self._type = _type
        self.position = position

    def clang(self) -> str:
        return f"{self._type.clang()} {self.decl.clang()}"


class FunctionDeclarationNode(Node):
    def __init__(self, name: str, arguments: Node, position: SourcePosition) -> None:
        self.name = name
        self.arguments = arguments
        self.position = position

    def clang(self) -> str:
        return f"{self.name} ( {self.arguments.clang()} )"


class ParameterNode(Node):
    def __init__(self, _type: Node, name: Node, position: SourcePosition) -> None:
        self._type = _type
        self.name = name
        self.position = position

    def clang(self) -> str:
        return f"{self._type.clang()} {self.name.clang()}"


class IncDecNode(Node):
    def __init__(self, value: Node, operand: str, position: SourcePosition) -> None:
        self.operand = operand
        super().__init__(value, position)

    def clang(self) -> str:
        return f"{self.value.clang()} {self.operand}"


class WhileNode(Node):
    def __init__(self, condition: Node, body: Node, position: SourcePosition) -> None:
        self.condition = condition
        self.body = body
        self.position = position

    def clang(self) -> str:
        return f"while ( {self.condition.clang()} ) {self.body.clang()}"


class ForNode(Node):
    def __init__(self, decl: Node, expr_1: Node, expr_2: Node, body: Node, position: SourcePosition) -> None:
        self.decl = decl
        self.expr_1 = expr_1
        self.expr_2 = expr_2
        self.body = body
        self.position = position

    def clang(self) -> str:
        return f"for ( {self.decl.clang()} ; {self.expr_1.clang()} ; {self.expr_2.clang()} ) {self.body.clang()}"


class IfElseNode(Node):
    def __init__(self, condition: Node, body: Node, else_body, position: SourcePosition) -> None:
        self.condition = condition
        self.body = body
        self.else_body = else_body
        self.position = position

    def clang(self) -> str:
        return f"if ( {self.condition.clang()} ) {self.body.clang()} else {self.else_body.clang()}"


class IfNode(Node):
    def __init__(self, condition: Node, body: Node, position: SourcePosition) -> None:
        self.condition = condition
        self.body = body
        self.position = position

    def clang(self) -> str:
        return f"if ( {self.condition.clang()} ) {self.body.clang()}"


class CompoundNode(Node):
    def __init__(self, value: Node, position: SourcePosition) -> None:
        super().__init__(value, position)

    def clang(self) -> str:
        return "{" + self.value.clang() + "}"


class JumpNode(Node):
    def __init__(self, value: Node, position: SourcePosition) -> None:
        super().__init__(value, position)

    def clang(self) -> str:
        return f"return {self.value.clang()} ;"


class DeclarationNode(Node):
    def __init__(self, _type: Node, name: Node, position: SourcePosition) -> None:
        self._type = _type
        self.name = name
        self.position = position

    def clang(self) -> str:
        return f"{self._type.clang()} {self.name.clang()}"


class DeclarationAssgnNode(Node):
    def __init__(self, _type: Node, name: Node, value: Node, position: SourcePosition) -> None:
        self._type = _type
        self.name = name
        super().__init__(value, position)

    def clang(self) -> str:
        return f"{self._type.clang()} {self.name.clang()} = {self.value.clang} ;"


class BinaryOpNode(Node):
    def __init__(self, operand: str, left: Node, right: Node, position: SourcePosition) -> None:
        self.operand = operand
        self.left = left
        self.right = right
        self.position = position

    def clang(self) -> str:
        return f"{self.left.clang()} {self.operand} {self.right.clang()}"


class CastNode(Node):
    def __init__(self, _type: Node, value: Node, position: SourcePosition) -> None:
        self._type = _type
        super().__init__(value, position)

    def clang(self) -> str:
        return f"({self._type.clang()}){self.value.clang()}"


class UnaryOpNode(Node):
    def __init__(self, operand: str, value: Node, position: SourcePosition) -> None:
        self.operand = operand
        super().__init__(value, position)

    def clang(self) -> str:
        return f"{self.operand}{self.value.clang()}"


class MemberAccessNode(Node):
    def __init__(self, name: Node, attribute: Node, position: SourcePosition) -> None:
        self.name = name
        self.attribute = attribute
        self.position = position

    def clang(self) -> str:
        return f"{self.name.clang()}.{self.attribute.clang()}"


class CallNode(Node):
    def __init__(self, call_name: Node, arguments: Node, position: SourcePosition) -> None:
        self.arguments = arguments
        self.call_name = call_name
        self.position = position

    def clang(self) -> str:
        return f"{self.call_name.clang()} ( {self.arguments.clang()} )"


class PointerNode(Node):
    def __init__(self, pointer: str, value: Node, position: SourcePosition) -> None:
        self.pointer = pointer
        super().__init__(value, position)

    def clang(self) -> str:
        return f"{self.pointer}{self.value.clang()}"


class TypeNode(Node):
    def __init__(self, value: str, position: SourcePosition) -> None:
        super().__init__(value, position)

    def clang(self) -> str:
        return self.value


class ValueNode(Node):
    def __init__(self, _type: None, value: str, position: SourcePosition) -> None:
        super().__init__(value, position)

    def clang(self) -> str:
        return self.value
