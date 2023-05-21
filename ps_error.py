from typing import List

class PS_Error:
    def __init__(self, msg: str, line: int, char: int) -> None:
        self.message: str = msg
        self.line: int = line
        self.char: int = char

    def add_ctx(self, lines: List[str]):
        new_msg: str = ""
        new_msg += lines[self.line-1]
        new_msg += " " * (self.char - 1) + "^" + "\n" # Yes this is valid
        new_msg += self.message + "\n"
        new_msg += f"line {self.line}; character {self.char}"
        self.message = new_msg

    def __str__(self) -> str:
        return self.message
