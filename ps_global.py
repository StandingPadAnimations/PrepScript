from typing import List, Union, Dict

class Global:
    def __init__(self):
        self.stack: List[Union[int, float, str, bool]] = []
        self.variables: List[Dict[str, Union[int, float, str, bool]]] = [{}]

    def push(self, val: Union[int, float, str, bool]):
        self.stack.append(val)

    def pop(self) -> Union[int, float, str, bool]:
        return self.stack.pop()

    def add_var(self, name: str, val: Union[int, float, str, bool]):
        self.variables[-1][name] = val

    def get_var(self, name: str):
        if name not in self.variables[-1]:
            return self.variables[0][name]
        else:
            return self.variables[-1][name]
