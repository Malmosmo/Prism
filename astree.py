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


class BracketNode(Node):
    def __init__(self, value: Node, brackets: str, position: SourcePosition) -> None:
        self.brackets = brackets
        super().__init__(value, position)

    def clang(self) -> str:
        return self.brackets[0] + self.value.clang() + self.brackets[1]


class CurlyNode(BracketNode):
    def __init__(self, value: Node, position: SourcePosition) -> None:
        super().__init__(value, "{}", position)


class CombinationNode(Node):
    def __init__(self, value: Node, value_2: Node, position: SourcePosition) -> None:
        self.value_2 = value_2
        super().__init__(value, position)

    def clang(self) -> str:
        if isinstance(self.value_2, EmptyNode):
            return self.value.clang()

        return f"{self.value.clang()} {self.value_2.clang()}"


# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------


class FunctionNode(Node):
    def __init__(self, _type: Node, signature: Node, body: Node, position: SourcePosition) -> None:
        self._type = _type
        self.signature = signature
        self.body = body
        self.position = position

    def clang(self) -> str:
        return f"{self._type.clang()} {self.signature.clang()} {self.body.clang()}"


class ExpressionNode(Node):
    def clang(self) -> str:
        return f"{self.value.clang()} ;"


class WhileNode(Node):
    def __init__(self, condition: Node, body: Node, position: SourcePosition) -> None:
        self.condition = condition
        self.body = body
        self.position = position

    def clang(self) -> str:
        return f"while ( {self.condition.clang()} ) {self.body.clang()}"


class DoWhileNode(WhileNode):
    def clang(self) -> str:
        return f"do {self.body.clang()} while ( {self.condition.clang()} ) ;"


class ForNode(Node):
    def __init__(self, declaration: Node, condition: Node, increment: Node, body: Node, position: SourcePosition) -> None:
        self.declaration = declaration
        self.condition = condition
        self.increment = increment
        self.body = body
        self.position = position

    def clang(self) -> str:
        return f"for ( {self.declaration.clang()} {self.condition.clang()} ; {self.increment.clang()} ) {self.body.clang()}"


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


class SwitchNode(Node):
    def __init__(self, condition: Node, value: Node, position: SourcePosition) -> None:
        self.condition = condition
        super().__init__(value, position)

    def clang(self) -> str:
        return f"switch ( {self.condition.clang()} ) {self.value.clang()}"


class CaseNode(Node):
    def __init__(self, case: Node, value: Node, position: SourcePosition) -> None:
        self.case = case
        super().__init__(value, position)

    def clang(self) -> str:
        return f"case {self.case.clang()} : {self.value.clang()}"


class CaseDefaultNode(Node):
    def clang(self) -> str:
        return f"default : {self.value.clang()}"


class JumpNode(Node):
    def __init__(self, _type: str,  value: Node, position: SourcePosition) -> None:
        self._type = _type
        super().__init__(value, position)

    def clang(self) -> str:
        if self._type in ["continue", "break"]:
            return self._type

        return f"return {self.value.clang()} ;"


# -----------------------------

class PointerNode(Node):
    def __init__(self, value: Node | str, position: SourcePosition) -> None:
        super().__init__(value, position)

    def clang(self) -> str:
        return f"*{self.value.clang()}"

# -----------------------------


class StructOrUnionNode(Node):
    def __init__(self, s_o_u: Node, ident: Node, decl: Node, position: SourcePosition) -> None:
        self.s_o_u = s_o_u
        self.ident = ident
        self.decl = decl
        self.position = position

    def clang(self) -> str:
        return f"{self.s_o_u.clang()} {self.ident.clang()} {{ {self.decl.clang()} }}"


class StructDeclarationNode(Node):
    def __init__(self, specifier: Node, declarator: Node, position: SourcePosition) -> None:
        self.specifier = specifier
        self.declarator = declarator
        self.position = position

    def clang(self) -> str:
        return f"{self.specifier.clang()} {self.declarator.clang()} ;"

# -----------------------------


class DesignationNode(Node):
    def __init__(self, value: Node, position: SourcePosition) -> None:
        super().__init__(value, position)

    def clang(self) -> str:
        return f"{self.value.clang()} = "


class DesignatorNode(Node):
    def __init__(self, value: Node | str, _type: int, position: SourcePosition) -> None:
        self._type = _type
        super().__init__(value, position)

    def clang(self) -> str:
        if self._type:
            return f".{self.value}"

        return f"[{self.value.clang()}]"

# -----------------------------


class EnumSpecifierNode(Node):
    def __init__(self, qualifier: Node, enum_list: Node, position: SourcePosition) -> None:
        self.qualifier = qualifier
        self.enum_list = enum_list
        self.position = position

    def clang(self) -> str:
        if isinstance(self.enum_list, EmptyNode):
            return self.qualifier.clang()

        return f"{self.qualifier.clang()} {self.enum_list.clang()}"


class EnumQualifierNode(Node):
    def __init__(self, value: str | EmptyNode, position: SourcePosition) -> None:
        super().__init__(value, position)

    def clang(self) -> str:
        if isinstance(self.value, EmptyNode):
            return "enum"

        return f"enum {self.value}"


class EnumeratorNode(Node):
    def __init__(self, enum_const: Node, const_expr: Node, position: SourcePosition) -> None:
        self.enum_const = enum_const
        self.const_expr = const_expr
        self.position = position

    def clang(self) -> str:
        if isinstance(self.const_expr, EmptyNode):
            return self.enum_const.clang()

        return f"{self.enum_const.clang()} = {self.const_expr.clang()}"

# -----------------------------

# TODO substitute by combination Node


class DirectDeclaratorNode(Node):
    def __init__(self, decl: Node, value: Node, position: SourcePosition) -> None:
        self.decl = decl
        super().__init__(value, position)

    def clang(self) -> str:
        return f"{self.decl.clang()} {self.value.clang()}"


class DeclaratorNode(Node):
    def __init__(self, ptr: Node, value: Node | str, position: SourcePosition) -> None:
        self.ptr = ptr
        super().__init__(value, position)

    def clang(self) -> str:
        if isinstance(self.ptr, EmptyNode):
            return self.value.clang()

        return f"{self.ptr.clang()} {self.value.clang()}"


class DeclarationNode(Node):
    def __init__(self, specifiers: Node, declaration_list: Node, position: SourcePosition) -> None:
        self.specifiers = specifiers
        self.declaration_list = declaration_list
        self.position = position

    def clang(self) -> str:
        return f"{self.specifiers.clang()} {self.declaration_list.clang()} ;"


class DeclaratorInitNode(Node):
    def __init__(self, declarator: Node, initalizer: Node, position: SourcePosition) -> None:
        self.declarator = declarator
        self.initalizer = initalizer
        self.position = position

    def clang(self) -> str:
        if isinstance(self.initalizer, EmptyNode):
            return self.declarator.clang()

        return f"{self.declarator.clang()} = {self.initalizer.clang()}"

# -----------------------------


class ConditionalNode(Node):
    def __init__(self, expr_1: Node, expr_2: Node, expr_3: Node, position: SourcePosition) -> None:
        self.expr_1 = expr_1
        self.expr_2 = expr_2
        self.expr_3 = expr_3
        self.position = position

    def clang(self) -> str:
        return f"{self.expr_1} ? {self.expr_2} : {self.expr_3}"


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


class ArrayAccessNode(Node):
    def __init__(self, postfix: Node, value: Node, position: SourcePosition) -> None:
        self.postfix = postfix
        super().__init__(value, position)

    def clang(self) -> str:
        return f"{self.postfix.clang()} [ {self.value.clang()} ]"


class FunctionCallNode(Node):
    def __init__(self, name: Node, parameters: Node, position: SourcePosition) -> None:
        self.name = name
        self.parameters = parameters
        self.position = position

    def clang(self) -> str:
        return f"{self.name.clang()} ( {self.parameters.clang()} )"


class AttributeNode(Node):
    def __init__(self, name: Node, attribute: str, position: SourcePosition) -> None:
        self.name = name
        self.attribute = attribute
        self.position = position

    def clang(self) -> str:
        return f"{self.name.clang()}.{self.attribute}"


class AttributeArrowNode(AttributeNode):
    def clang(self) -> str:
        return f"{self.name.clang()} -> {self.attribute}"


class ArrayNode(Node):
    def __init__(self, _type: Node, value: Node, position: SourcePosition) -> None:
        self._type = _type
        super().__init__(value, position)

    def clang(self) -> str:
        return f"({self._type.clang()}) {{ {self.value.clang()} }}"


class SizeOfNode(Node):
    def __init__(self, value: Node | str, position: SourcePosition) -> None:
        super().__init__(value, position)

    def clang(self) -> str:
        return f"sizeof({self.value.clang()})"


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
