from enum import Enum
from typing import List, Optional
from dataclasses import astuple, dataclass
class Token(Enum):
    KEYWORD = 0
    IDENT = 1
    LPAREN = 2
    RPAREN = 3
    EQUAL = 4

    INT = 5
    FLOAT = 6
    STRING = 7
    BOOL = 8

@dataclass
class Lexeme:
    token: Token
    value: str
    line: int
    char: int

    def __iter__(self):
        return iter(astuple(self))

class State(Enum):
    NORMAL = 0
    STRING = 1

KEYWORDS = [
    "let"
]

class Lexer(object):
    def __init__(self) -> None:
        self.buffer: str = ""
        self.tokens: List[Lexeme] = []
        self.state: State = State.NORMAL
        self.i_line: int = 1
        self.i_char: int = 1

    def num_token(self) -> Optional[Token]:
        try:
            int(self.buffer)
            return Token.INT
        except ValueError:
            try:
                float(self.buffer)
                return Token.FLOAT
            except ValueError:
                pass
        return None


    def tokenize_buffer(self):
        if self.state == State.STRING:
            self.tokens.append(Lexeme(Token.STRING, self.buffer, self.i_line, self.i_char - len(self.buffer)))
        else:
            if len(self.buffer):
                if self.buffer in KEYWORDS:
                    self.tokens.append(Lexeme(Token.KEYWORD, self.buffer, self.i_line, self.i_char - len(self.buffer)))
                elif isinstance(self.num_token(), Token):
                    self.tokens.append(Lexeme(self.num_token(), self.buffer, self.i_line, self.i_char - len(self.buffer)))
                else:
                    self.tokens.append(Lexeme(Token.IDENT, self.buffer, self.i_line, self.i_char - len(self.buffer)))
        self.buffer = ""

    def lexer(self, lines: List[str]) -> List[Lexeme]:
        for line in lines:
            for char in line:
                if self.state == State.STRING and char != '"':
                    self.buffer += char
                    continue
                if char == "(":
                    self.tokenize_buffer()
                    self.tokens.append(Lexeme(Token.LPAREN, char, self.i_line, self.i_char))
                elif char == ")":
                    self.tokenize_buffer()
                    self.tokens.append(Lexeme(Token.RPAREN, char, self.i_line, self.i_char))
                elif char == "=":
                    self.tokenize_buffer()
                    self.tokens.append(Lexeme(Token.EQUAL, char, self.i_line, self.i_char))
                elif char == " " or char == "\n":
                    self.tokenize_buffer()
                elif char == '"':
                    if self.state == State.NORMAL:
                        self.state = State.STRING
                    elif self.state == State.STRING:
                        self.tokenize_buffer()
                        self.state = State.NORMAL 
                else:
                    self.buffer += char
                self.i_char += 1
            self.i_line += 1
            self.i_char = 1
        return self.tokens
