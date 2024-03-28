from dataclasses import dataclass
from errors import handleError
from tokens import Tokens

@dataclass
class Token:
    ttype : Tokens
    tval : str | None

class Tokenizer:
    def __init__(self, _source, begin=0) -> None:
        self.source = _source
        self.index = begin

    def tokenize(self, nextbegin=0) -> list[Token]:
        tokens = []
        buf = ""

        while self.peek() is not None:
            if self.peek().isalpha():
                buf += self.consume()
                while self.peek() is not None and self.peek().isalnum():
                    buf += self.consume()
                # check keywords
                if buf == "exit":
                    tokens.append(Token(Tokens.EXIT, None))
                    buf = ""
                    continue
                elif buf == "let":
                    tokens.append(Token(Tokens.LET, None))
                    buf = ""
                    continue
                elif buf == "add":
                    tokens.append(Token(Tokens.ADD, None))
                    buf = ""
                    continue
                elif buf == "sub":
                    tokens.append(Token(Tokens.SUB, None))
                    buf = ""
                    continue
                else:
                    tokens.append(Token(Tokens.IDENT, buf))
                    buf = ""
                    continue
            elif self.peek().isdigit():
                buf += self.consume()
                while self.peek() is not None and self.peek().isdigit():
                    buf += self.consume()
                tokens.append(Token(Tokens.INT_LIT, buf))
                buf = ""
                continue
            elif self.peek() == ";":
                tokens.append(Token(Tokens.SEMI, None))
                self.consume()
                buf = ""
                continue
            elif self.peek() == "(":
                tokens.append(Token(Tokens.OPENPAREN, None))
                self.consume()
                buf = ""
                continue
            elif self.peek() == ")":
                tokens.append(Token(Tokens.CLOSEPAREN, None))
                self.consume()
                buf = ""
                continue
            elif self.peek() == ",":
                tokens.append(Token(Tokens.COMMA, None))
                self.consume()
                buf = ""
                continue
            elif self.peek() == "=":
                tokens.append(Token(Tokens.EQ, None))
                self.consume()
                buf = ""
                continue
            elif self.peek().isspace():
                self.consume()
                continue
            else:
                handleError(6)

        self.index = nextbegin
        return tokens

    def peek(self, ahead=1) -> str | None:
        if self.index + ahead - 1 >= len(self.source):
            return None
        return self.source[self.index + ahead - 1]

    def consume(self) -> str:
        self.index += 1
        return self.source[self.index-1]
