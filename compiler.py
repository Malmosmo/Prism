from _parser import ParserState, Parser
from lexer import tokenize, TOKENTYPES
from preprocessor import preprocess


def compile_c(inFile, outFile):
    with open(inFile, "r") as file:
        source = file.read()

    # source = preprocess(source)

    state = ParserState(inFile, source)

    source = preprocess(source)

    tokens = tokenize(state)

    parser = Parser(TOKENTYPES, [])

    ast = parser.parse(tokens, state)

    ccode = ast.clang()

    with open(outFile, "w") as file:
        file.write(ccode)
