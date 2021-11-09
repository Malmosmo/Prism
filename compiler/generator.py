class CodeGenerator:
    def __init__(self, ast) -> None:
        self.output = "" + self.generate(ast)

    def generate(self, node):
        method_name = f"gen_{node.__class__.__name__}"

        method = getattr(self, method_name, None)

        if not method:
            print(method_name, "not implemented")

            return "None"

        else:
            return method(node)

    ##################################################
    # Program
    ##################################################
    def gen_ProgramNode(self, node):
        return "package main\n\n" + self.generate(node.value)

    ##################################################
    # Functions
    ##################################################
    def gen_FuncNode(self, node):
        return f"func {node.name} () {self.generate(node.type)} {{\n{self.generate(node.body)}\n{self.generate(node.return_value)}\n}}"

    def gen_VoidFuncNode(self, node):
        return f"func {node.name} () {{\n{self.generate(node.body)}\n}}"

    ##################################################
    # Builtin Functions
    ##################################################
    def gen_BuiltinFunctionNode(self, node):
        if node.func == "print":
            return f"println({self.generate(node.value)})"

        return None

    ##################################################
    # Return
    ##################################################
    def gen_ReturnNode(self, node):
        return f"return {self.generate(node.value)}"

    ##################################################
    # Block
    ##################################################
    def gen_BlockNode(self, node):
        return "\n".join(self.generate(cmd_node) for cmd_node in node.commands)

    ##################################################
    # Types
    ##################################################
    def gen_TypeNode(self, node):
        return node.value

    ##################################################
    # Literals
    ##################################################
    def gen_IntegerNode(self, node):
        return f"{node.value.getstr()}"
