import sys

from rply.token import SourcePosition


class Error:
    def __init__(self, position: SourcePosition, filename: str, source: str, message: str) -> None:
        self.position =  position if position else SourcePosition(0, 0, 0)
        self.filename = filename
        self.source = source
        self.message = message

        self.raiseError()

    def raiseError(self):
        print(str(self))

        sys.exit(1)

    def __str__(self) -> str:
        lines = self.source.splitlines()
        lineno = self.position.lineno

        output = f"FILE {self.filename}, line {lineno}\n"

        # output += f"{self.position.lineno - 1:03}| " + lines[self.position.lineno - 1] + "\n"
        output += f"{self.position.lineno:03}|>" + lines[self.position.lineno] + "\n"
        output += "-" * (self.position.colno + 4) + "^" + "\n"
        # output += f"{self.position.lineno + 1:03}| " + lines[self.position.lineno + 1] + "\n"

        output += f"{self.__class__.__name__}: " + self.message + "\n"

        return output


class LexerError(Error):
    pass


class InvalidSyntaxError(Error):
    pass


class UnexpectedEndError(Error):
    pass
