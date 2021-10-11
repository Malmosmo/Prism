# from .interpreter import Context
from rply.token import SourcePosition
import sys


##################################################
# Errors
##################################################
class Error(Exception):
    def __init__(self, position: SourcePosition, filename: str, source: str, name: str, details: str) -> None:
        self.position = position
        self.filename = filename
        self.source = source.splitlines()
        self.name = name
        self.details = details

    def raise_error(self):
        print(self)
        sys.exit()

    def __str__(self) -> str:
        result = ""

        if self.position is None:
            line_number = len(self.source)
            col_number = len(self.source[-1])

        else:
            line_number = self.position.lineno
            col_number = self.position.colno - 1

        result += f"  File \"{self.filename}\", line {line_number}\n"
        result += f"    {self.source[line_number - 1]}\n"
        result += "    " + " " * col_number + "^\n"
        result += f"\n{self.name}: {self.details}"

        return result


class InvalidSynatxError(Error):
    def __init__(self, position: SourcePosition, filename: str, source: str, details: str) -> None:
        super().__init__(position, filename, source, "InvalidSynatx", details)
        self.raise_error()


class UnexpectedEndError(Error):
    def __init__(self, position: SourcePosition, filename: str, source: str, details: str) -> None:
        super().__init__(position, filename, source, "UnexpectedEnd", details)
        self.raise_error()


##################################################
# UnaryOp
##################################################
class RTError(Error):
    def __init__(self, position: SourcePosition, filename: str, source: str, name: str, details: str, context) -> None:
        super().__init__(position, filename, source, name, details)
        self.context = context

    def __str__(self) -> str:
        result = self.traceback()
        result += f"\n{self.name}: {self.details}"

        return result

    def traceback(self):
        result = ""
        ctx = self.context

        while ctx:
            pos = ctx.position
            result = "    " + self.source[pos.lineno + 1] + "\n" + result
            result = f'  File "{self.filename}", line {pos.lineno + 1}, in {ctx.name}\n' + result
            ctx = ctx.parent

        result += "    " + " " * (self.position.colno - 1) + "^\n"
        return 'Traceback (most recent call last):\n' + result


class InvalidTypeError(RTError):
    def __init__(self, position: SourcePosition, filename: str, source: str, name: str, details: str, context) -> None:
        super().__init__(position, filename, source, name, details, context)


class DivisionByZeroError(RTError):
    def __init__(self, position: SourcePosition, filename: str, source: str, name: str, details: str, context) -> None:
        super().__init__(position, filename, source, name, details, context)
