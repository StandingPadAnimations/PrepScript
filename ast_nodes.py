from dataclasses import dataclass, field
from typing import List, Type, Union, Dict
from bytecode import FUNC_CALL, BYTECODE, LOAD_NAME, PUSH, STORE_NAME
from ps_error import PS_Error

# Base node class
@dataclass
class Expr:
    line: int
    char: int
    def compile(self) -> List[Type[BYTECODE]]:
        return []

# Represents an int
@dataclass
class Int(Expr):
    constant: int

    def compile(self) -> List[Type[BYTECODE]]:
        return [PUSH(self.constant)]

# Represants a float
@dataclass
class Float(Expr):
    constant: float

    def compile(self) -> List[Type[BYTECODE]]:
        return [PUSH(self.constant)]

# Represants a string
@dataclass
class String(Expr):
    constant: str

    def compile(self) -> List[Type[BYTECODE]]:
        return [PUSH(self.constant)]

# Represents a boolean
@dataclass
class Bool(Expr):
    constant: bool
    
    def compile(self) -> List[Type[BYTECODE]]:
        return [PUSH(self.constant)]

# Represents an identifier
@dataclass
class Ident(Expr):
    name: str

    def compile(self) -> List[Type[BYTECODE]]:
        return [LOAD_NAME(self.name)]

# Represents a variable declaration
@dataclass
class VariableDeclaration(Expr):
    variable: str
    value: Type[Expr]

    def compile(self) -> List[Type[BYTECODE]]:
        return self.value.compile() + [STORE_NAME(self.variable)]

@dataclass
class FunctionCall(Expr):
    function: str
    args: List[Type[Expr]] = field(default_factory=list)
    
    def compile(self) -> List[Type[BYTECODE]]:
        return [arg.compile()[-1] for arg in self.args] + [FUNC_CALL(self.function)]

# The entire program
@dataclass 
class Program:
    program: List[Type[Expr]] = field(default_factory=list) 

    def compile(self) -> Union[List[Type[BYTECODE]], PS_Error]:
        bytecode: List[Type[BYTECODE]] = []
        variables: List[Dict[str, Expr]] = [{}]
        for node in self.program:
            if isinstance(node, VariableDeclaration):
                if node.variable in variables[-1]:
                    return PS_Error("Can not redeclare a variable!", node.line, node.char)
                if isinstance(node.value, Ident):
                    if node.value.name not in variables[-1] or node.value.name not in variables[0]:
                        return PS_Error(f"{node.value.name} not declared! Perhaps you made a mistake?", node.value.line, node.value.char)
            bytecode += node.compile()
        return bytecode

    def push(self, node: Type[Expr]):
        self.program.append(node)

