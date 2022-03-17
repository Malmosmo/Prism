from lexer import Lexer
from Pparser import Parser, ParserState


KEYWORDS = {
    "INT": r"int(?!\w)",
    "RETURN": r"return(?!\w)",
    "IF": r"if(?!\w)",
    "ELSE": r"else(?!\w)",
    "WHILE": r"while(?!\w)",
    "FOR": r"for(?!\w)",
    "CONST": r"const(?!\w)",
    "CLASS": r"class(?!\w)",
}

OPERATORS = {
    "INC": r"\+\+",
    "DEC": r"\-\-",

    "DOT": r"\.",

    "+=": r"\+=",
    "-=": r"-=",
    "*=": r"\*=",
    "/=": r"/=",

    "MODEQ": r"%=",
    "&=": r"&=",
    "^=": r"^=",
    "LOREQ": r"\|=",

    "LSHIFT": r"\<\<",
    "RSHIFT": r"\>\>",

    "LSHIFTEQ": r"\<\<\=",
    "RSHIFTEQ": r"\>\>\=",

    "==": r"\=\=",
    "!=": r"\!\=",
    "<=": r"\<\=",
    ">=": r"\>\=",

    "LAND": r"\&\&",
    "LOR": r"\|\|",

    "=": r"\=",
    "!": r"\!",
    "<": r"\<",
    ">": r"\>",

    "+": r"\+",
    "-": r"\-",
    "*": r"\*",
    "/": r"\/",

    "MOD": r"\%",
    "&": r"\&",
    "CARROT": r"\^",
    "OR": r"\|",
}

LITERALS = {
    "INTEGER": r"\d+",
    "STRING": r'\"[^\"]*\"',
}

PUNCTUATORS = {
    "(": r"\(",
    ")": r"\)",

    "{": r"\{",
    "}": r"\}",

    # "[": r"\[",
    # "]": r"\]",

    ",": r"\,",
    ";": r"\;",
}

IDENTIFIERS = {
    "IDENTIFIER": r"[_a-zA-Z][_a-zA-Z0-9]{0,31}",
}

TOKENTYPES = KEYWORDS | OPERATORS | LITERALS | PUNCTUATORS | IDENTIFIERS


if __name__ == "__main__":
    Template = """package main\n\n"""

    with open("input.prism", "r") as in_file:
        source = in_file.read()

    if len(source) > 0:
        lexer = Lexer(TOKENTYPES, r'[ \n\t\r\f\v]+')
        tokens = lexer.lex(source)

        # for token in lexer.lex(source):
        #     print(token)

        # quit()
        state = ParserState("input.prism", source)
        parser = Parser(list(TOKENTYPES), [])

        ast = parser.parse(tokens, state)

        with open("out/main.c", "w") as out_file:
            # out_file.write(Template + ast.generate())
            out_file.write(ast.clang())
