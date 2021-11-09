from compiler.generator import CodeGenerator
from compiler.lexer import Lexer
from compiler.parser import Parser, ParserState


KEYWORDS = {
    "TYPE_INT": r"int(?!\w)",
    "RETURN": r"return(?!\w)"
}

OPERATORS = {
    "=": r"\=",
}

CONSTANTS = {
    "INTEGER": r"\d+",
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
        parser = Parser(list(TOKENTYPES), [], file, source)

        ast = parser.parse(tokens, state)

        code_gen = CodeGenerator(ast)

        with open("./out/test.go", "w") as f:
            f.write(code_gen.output)

        return code_gen.output
