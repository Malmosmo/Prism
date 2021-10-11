from __future__ import annotations
from rply.token import BaseBox, SourcePosition, Token


class Node(BaseBox):
    def __init__(self, value: Node, position: SourcePosition) -> None:
        self.value = value
        self.position = position

    def rep(self):
        return f"{self.__class__.__name__}({self.value.rep()})"

    def getsourcepos(self):
        return self.position

##################################################
# Block Statements
##################################################
