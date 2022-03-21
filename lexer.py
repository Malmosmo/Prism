# --------------------------------------------------------------------------------------------------
# https://github.com/knowknowledge/Python-C-Parser
# https://github.com/interpreters/pypreprocessor
# --------------------------------------------------------------------------------------------------

from __future__ import annotations
from typing import Generator

import string
from enum import Enum

from rply.token import SourcePosition, Token

from errors import LexerError
from util import ParserState

# --------------------------------------------------------------------------------------------------

types = ["short", "int", "long", "float", "double", "char", "void"]  # removed FILE, BOOL
containers = ["enum", "struct", "union", "typedef"]
modifiers = ["const", "volatile", "extern", "static", "register", "signed", "unsigned", "auto", "restrict"]  # added AUTO, RESTRICT
flow = ["if", "else",
        "case", "default",
        "continue", "break"]  # removed GOTO
loops = ["for", "do", "while", "switch"]
keywords = types + containers + modifiers + flow + loops + ["return", "sizeof"]

prefix_operations = ["-", "+", "*", "&", "~", "!"]  # removed ++ , --
postfix_operations = ["++", "--"]
selection_operations = [".", "->"]  # Left-to-Right
multiplication_operations = ["*", "/", "%"]  # Left-to-Right
addition_operations = ["+", "-"]  # Left-to-Right
bitshift_operations = ["<<", ">>"]  # Left-to-Right
relation_operations = ["<", "<=", ">", ">="]  # Left-to-Right
equality_operations = ["==", "!="]  # Left-to-Right
bitwise_operations = ["&", "^", "|"]  # Left-to-Right
logical_operations = ["&&", "||"]
ternary_operations = ["?", ":"]
# Ternary () ? () : ()
assignment_operations = ["=",  # Right-to-Left
                         "+=", "-=",
                         "/=", "*=", "%=",
                         "<<=", ">>=",
                         "&=", "^=", "|=",
                         ]
binary_operations = multiplication_operations + \
    addition_operations + \
    bitshift_operations + \
    relation_operations + \
    equality_operations + \
    bitwise_operations + \
    logical_operations + \
    assignment_operations + selection_operations

ellipsis = ["..."]

operators = prefix_operations + postfix_operations + binary_operations + ternary_operations + ellipsis

# --------------------------------------------------------------------------------------------------

TOKENTYPES = [token.upper() for token in keywords +
              operators +
              ["IDENTIFIER", "STRING", "CONSTANT", "TypedIdent", "INLINE"] +
              ["[", "]", "(", ")", "{", "}", ";", ","] +
              ["PRAGMA"]]
# missing: $ \ @ `

# --------------------------------------------------------------------------------------------------

# error in parser if used directly
SUBSTITUTE = {
    "|": "OR",
    "||": "LOR",
    "|=": "OREQ",
    ":": "DDOT",
}

TOKENTYPES = [SUBSTITUTE[token] if token in SUBSTITUTE else token for token in TOKENTYPES]

# --------------------------------------------------------------------------------------------------

typedef = False
customTypes = []


class TokenType(Enum):
    UNSET = 0
    COMMENT = 1
    PRAGMA = 2
    CHAR = 3
    STRING = 4
    NUMBER = 5
    OPERATOR = 6


def consists_of(value, chars):
    return len(value) and all(map(lambda char: char in chars, value))


def tokenize(state: ParserState) -> Generator[Token, None, None]:
    symbols = string.punctuation.replace("_", "")
    floatdigits = string.digits + "."

    line = 0
    column = 0

    token = ""
    tokentype = TokenType.UNSET

    def _token():
        global typedef, customTypes

        if typedef and token == ";":
            typedef = False

        if tokentype == TokenType.STRING:
            return Token("STRING", token, SourcePosition(0, line, column))

        elif tokentype == TokenType.PRAGMA:
            return Token("PRAGMA", token, SourcePosition(0, line, column))

        elif token in operators or token in symbols:
            if token in SUBSTITUTE:
                return Token(SUBSTITUTE[token], token, SourcePosition(0, line, column))

            return Token(token, token, SourcePosition(0, line, column))

        elif tokentype == TokenType.CHAR or token[0] in floatdigits:
            return Token("CONSTANT", token, SourcePosition(0, line, column))

        elif token in keywords:
            if token == "typedef":
                typedef = True

            return Token(token.upper(), token, SourcePosition(0, line, column))

        elif token in customTypes:
            return Token("TYPEDIDENT", token, SourcePosition(0, line, column))

        if typedef:
            customTypes.append(token)

        return Token("IDENTIFIER", token, SourcePosition(0, line, column))

    for char in state.source:
        column += 1

        # comment
        if tokentype == TokenType.COMMENT:
            if char == "\n":
                if token.startswith("//"):
                    token = ""
                    tokentype = TokenType.UNSET

                line += 1
                column = 0

            elif char == "/" and token.endswith("*") and not token.startswith("//"):
                token = ""
                tokentype = TokenType.UNSET

            else:
                token += char

        # pragma
        elif tokentype == TokenType.PRAGMA:
            if char == "\n":
                yield _token()
                token = ""
                tokentype = TokenType.UNSET

                line += 1
                column = 0

            else:
                token += char

        # string start and end
        elif char == '"' and tokentype != TokenType.CHAR:
            # start
            if tokentype != TokenType.STRING:
                if token != "":
                    yield _token()

                token = char
                tokentype = TokenType.STRING

            # escape characters
            elif len(token) and token.endswith("\\"):
                token += '"'

            # end
            else:
                tokentype = TokenType.STRING
                token += char
                yield _token()
                token = ""
                tokentype = TokenType.UNSET

        # in string
        elif tokentype == TokenType.STRING:
            if token.endswith("\\"):
                # escape char
                pass

            token += char

        # in char / char end
        elif tokentype == TokenType.CHAR:
            if token.endswith("\\"):
                # escape
                token += char

            # end
            elif char == "'":
                token += char

                if len(token) != 3:
                    LexerError(SourcePosition(0, line, column), state.filename, state.source, f"Character {token} to long!")

                yield _token()

                token = ""
                tokentype = TokenType.UNSET

            # in
            else:
                token += char

        # char start
        elif char == "'" and tokentype != TokenType.STRING:
            if token != "":
                yield _token()

            token = char
            tokentype = TokenType.CHAR

        # pragma start
        elif char == "#":
            if token != "":
                yield _token()

            token = char
            tokentype = TokenType.PRAGMA

        # comment start
        elif token == "/" and char in "*/":
            token += char
            tokentype = TokenType.COMMENT

        # special characters
        elif char in symbols:
            if token + char in operators:
                token += char
                tokentype = TokenType.OPERATOR

            elif char == "." and consists_of(token, string.digits):
                token += char

            else:
                if token != "":
                    yield _token()

                token = char

        # digit or letter + '_'
        else:
            if consists_of(token, symbols):
                yield _token()

                token = ""
                tokentype = TokenType.UNSET

            if char in string.whitespace:
                if token != "":
                    yield _token()

                if char == "\n":
                    line += 1
                    column = 0

                token = ""
                tokentype = TokenType.UNSET

            else:
                token += char

    if token not in string.whitespace:
        if tokentype != TokenType.COMMENT:
            yield _token()


if __name__ == "__main__":
    source = """
        switch (2 < 3) {
        case 1 : {
            printf("CASE 1");
            break;
        }
        case 0: {
            printf("CASE 0");
            break;
        }
 
    }
 
    """

    print(list(tokenize(ParserState("<>", source))))

    # print(TOKENTYPES)
