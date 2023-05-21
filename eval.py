from typing import Callable, Dict, List, Type
import bytecode
import prepscript_funcs
from ps_global import Global

BUILT_INS: Dict[str, Callable[[Global], None]] = {
    "print" : prepscript_funcs.print_ps
}

def eval(bytecode_vec: List[Type[bytecode.BYTECODE]]):
    global_s: Global = Global()
    ip: int = 0
    while ip < len(bytecode_vec):
        ins = bytecode_vec[ip]
        if isinstance(ins, bytecode.PUSH):
            global_s.push(ins.expression)
        if isinstance(ins, bytecode.POP):
            global_s.pop()
        if isinstance(ins, bytecode.FUNC_CALL):
            BUILT_INS[ins.func](global_s)
        if isinstance(ins, bytecode.STORE_NAME):
            global_s.add_var(ins.name, global_s.pop())
        if isinstance(ins, bytecode.LOAD_NAME):
            global_s.push(global_s.get_var(ins.name))
        ip += 1
