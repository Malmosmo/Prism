from compiler.main import Compiler

tokens = Compiler.compile("prism/sample.prism")

for token in tokens:
    print(token)
