from compiler.main import Compiler

ast = Compiler.compile("prism/sample.prism")

print(ast)
