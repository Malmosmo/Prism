from compiler.lexer import Lexer
from compiler.parser import Parser, ParserState


KEYWORDS = {
    "TYPE_INT": r"int(?!\w)",
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

        lexer = Lexer(TOKENTYPES, r'[ \n\t\r\f\v]+')

        tokens = lexer.lex(source)

        state = ParserState()
        parser = Parser(list(TOKENTYPES), [], file, source)

        ast = parser.parse(tokens, state)

        return ast.rep()
