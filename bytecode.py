from dataclasses import dataclass
from typing import Union

class BYTECODE:
    pass

@dataclass
class PUSH(BYTECODE):
    expression: Union[int, float, str, bool]

class POP(BYTECODE):
    pass

@dataclass
class STORE_NAME(BYTECODE):
    name: str

@dataclass
class LOAD_NAME(BYTECODE):
    name: str

@dataclass
class FUNC_CALL(BYTECODE):
    func: str
