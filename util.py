
class ParserState:
    def __init__(self, filename: str, source: str):
        self.filename = filename
        self.source = source

        self.traceback = ""
