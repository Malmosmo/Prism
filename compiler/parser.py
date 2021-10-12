from rply import ParserGenerator
from rply.token import Token
from compiler.errors import *
from compiler.ast import *


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
        # Program
        ##################################################
        @self.pg.production('program : func')
        def prgm(state: ParserState, p):
            return ProgramNode(p[0], p[0].getsourcepos())

        ##################################################
        # Functions
        ##################################################
        @self.pg.production('func : type IDENTIFIER ( ) { stmt }')
        def func(state: ParserState, p):
            return FuncNode(p[0], p[1].getstr(), p[5], p[0].getsourcepos())

        ##################################################
        # Types
        ##################################################
        @self.pg.production('type : INT')
        def type_int(state: ParserState, p):
            return TypeIntNode(p[0].getstr(), p[0].getsourcepos())

        ##################################################
        # Statement
        ##################################################
        @self.pg.production('stmt : assg ;')
        def stmt(state: ParserState, p):
            return p[0]

        ##################################################
        # Assign
        ##################################################
        @self.pg.production('assg : IDENTIFIER = expr')
        def assg(state: ParserState, p):
            return AssignNode(p[0].getstr(), p[2], p[0].getsourcepos())

        ##################################################
        # Expressions
        ##################################################
        @self.pg.production('expr : ( expr )')
        def expr_self(state: ParserState, p):
            return p[1]

        @self.pg.production('expr : INTEGER')
        def expr_int(state: ParserState, p):
            return IntegerNode(p[0], p[0].getsourcepos())

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
