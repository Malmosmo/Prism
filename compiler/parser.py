from rply import ParserGenerator
from rply.token import Token
from .errors import *


class ParserState:
    def __init__(self):
        pass

    def add_variable(self, var):
        self.variables.append(var)

    def add_constant(self, var):
        self.constants.append(var)


class Parser:
    def __init__(self, tokens: list, precedence: list, filename: str, source: str) -> None:
        self.pg = ParserGenerator(tokens, precedence)
        self.parser = self.init()
        self.filename = filename
        self.source = source

    def init(self):

        ##################################################
        # Errors
        ##################################################
        @self.pg.error
        def error_handler(state: ParserState, token: Token):
            pos = token.getsourcepos()

            if pos:
                InvalidSynatxError(
                    pos,
                    self.filename,
                    self.source,
                    f"Unexpected Token: {token.name}"
                )

            elif token.gettokentype() == '$end':
                UnexpectedEndError(
                    pos,
                    self.filename,
                    self.source,
                    f"Unexpected End"
                )

            else:
                InvalidSynatxError(
                    self.filename,
                    self.source,
                    f"Unexpected Token: {token.name}"
                )

        return self.pg.build()

    def parse(self, text: str, state: ParserState = None):
        return self.parser.parse(text, state)
