from enum import Enum, auto

# TOKEN TYPES
class Tokens (Enum):
    EXIT = auto()
    INT_LIT = auto()
    SEMI = auto()
    OPENPAREN = auto()
    CLOSEPAREN = auto()
    COMMA = auto()
    LET = auto()
    IDENT = auto()
    EQ = auto()
    ADD = auto()
    SUB = auto()
