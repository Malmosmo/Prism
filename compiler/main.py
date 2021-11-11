import subprocess

from compiler.generator import CodeGenerator
from compiler.lexer import Lexer
from compiler.parser import Parser, ParserState


KEYWORDS = {
    "PRINT": r"print(?!\w)",

    "TYPE_INT": r"int(?!\w)",
    "TYPE_STR": r"string(?!\w)",

    "RETURN": r"return(?!\w)",
}

OPERATORS = {
    "=": r"\=(?!\w)",
    "+": r"\+(?!\w)",
    "-": r"\-(?!\w)",
    "*": r"\*(?!\w)",
    "/": r"\/(?!\w)",
}

CONSTANTS = {
    "INTEGER": r"\d+",
    "STRING": r'\"[^\"]*\"',
}

PUNCTUATORS = {
    "(": r"\(",
    ")": r"\)",

    "{": r"\{",
    "}": r"\}",

    ";": r"\;",
}

IDENTIFIERS = {
    "IDENTIFIER": r"[_a-zA-Z][_a-zA-Z0-9]{0,31}",
}

TOKENTYPES = KEYWORDS | OPERATORS | CONSTANTS | PUNCTUATORS | IDENTIFIERS


class Compiler:
    @staticmethod
    def compile(file: str):
        with open(file, 'r') as f:
            source = f.read()

        # lex
        lexer = Lexer(TOKENTYPES, r'[ \n\t\r\f\v]+')
        tokens = lexer.lex(source)

        # parser
        state = ParserState()
        parser = Parser(list(TOKENTYPES), [
            ('left', ['+', '-']),
            ('left', ['*', '/']),
        ], file, source)

        ast = parser.parse(tokens, state)

        # code_gen = CodeGenerator(ast)
        output = ast.generate()

        with open("./out/test.go", "w") as f:
            f.write(output)

        # response = subprocess.Popen(["go", "build", "-o", "./bin/out.exe", "./out/test.go"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # print("----------------------")
        # print(response.stdout.read())
        # print(response.stderr.read())
        # print("----------------------")

        return output
