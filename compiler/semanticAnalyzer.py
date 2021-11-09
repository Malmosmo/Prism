from compiler.ast import *


class TypeChecker:
    def __init__(self, ast):
        self.ast = ast

    def check(self, node):
        if type(node) == FuncNode:
            func_type = node.type
            return_type = self.check(node.return_value)

            print(func_type, return_type)

            return func_type

        elif type(node) == IntegerNode:
            return TypeIntNode("int")
