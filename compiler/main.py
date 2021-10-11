from compiler.lexer import Lexer


KEYWORDS = {
    "INT": r"int(?!\w)",
}

OPERATORS = {
    "ASSIGN": r"\=",
}

CONSTANTS = {
    "INTEGER": r"\d+",
}

PUNCTUATORS = {
    "SEMICOLON": r"\;",
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

        return tokens
