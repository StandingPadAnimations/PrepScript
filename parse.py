from typing import List, Union, Type
from lex import Token, Lexeme
import ast_nodes
from ps_error import PS_Error

class Parser:
    def __init__(self, tokens: List[Lexeme]) -> None:
        self.ast: ast_nodes.Program = ast_nodes.Program()
        self.tokens: List[Lexeme] = tokens
        self.index: int = 0
        self.token, self.expression, self.line, self.char = self.tokens[self.index]
    
    def incr(self) -> bool:
        self.index += 1
        if self.index < len(self.tokens):
            self.token, self.expression, self.line, self.char = self.tokens[self.index]
            return True
        return False

    def parse(self) -> Union[ast_nodes.Program, PS_Error]:
        while self.index < len(self.tokens):
            if self.token == Token.IDENT:
                res = self.ident_handler(self.expression)
                if isinstance(res, PS_Error):
                    return res
                else:
                    self.ast.push(res)
            elif self.token == Token.KEYWORD:
                res = self.keyword_handler(self.expression)
                if isinstance(res, PS_Error):
                    return res
                else:
                    self.ast.push(res)
            self.incr()
        return self.ast
    
    def keyword_handler(self, keyword: str) -> Union[Type[ast_nodes.Expr], PS_Error]:
        if keyword == "let":
            self.incr()
            if self.token is not Token.IDENT:
                return PS_Error(f"Expected identifier, got {self.token.name}", self.line, self.char)
            ident = self.expression
            self.incr()
            if self.token is not Token.EQUAL:
                return PS_Error(f"Expected equal sign, got {self.token.name}", self.line, self.char)
            self.incr()
            c_node = self.const_hander()
            if isinstance(c_node, PS_Error):
                return c_node
            return ast_nodes.VariableDeclaration(self.line, self.char, ident, c_node)

    def ident_handler(self, ident: str) -> Union[Type[ast_nodes.Expr], PS_Error]:
        self.incr()
        if self.token == Token.LPAREN:
            node = ast_nodes.FunctionCall(self.line, self.char, ident)
            self.incr()
            while self.token != Token.RPAREN:
                arg_node = self.const_hander()
                if isinstance(arg_node, PS_Error):
                    return arg_node
                node.args.append(arg_node)
                if not self.incr():
                    return PS_Error("Function call must be closed with ')'", node.line, node.char)
            return node

    def const_hander(self) -> Union[Type[ast_nodes.Expr], PS_Error]:
        if self.token == Token.INT:
            return ast_nodes.Int(self.line, self.char, int(self.expression))
        elif self.token == Token.FLOAT:
            return ast_nodes.Float(self.line, self.char, float(self.expression))
        elif self.token == Token.STRING:
            return ast_nodes.String(self.line, self.char, self.expression)
        elif self.token == Token.BOOL:
            return ast_nodes.Bool(self.line, self.char, bool(self.expression))
        elif self.token == Token.IDENT:
            return ast_nodes.Ident(self.line, self.char, self.expression)
        else:
            return PS_Error(f"Expected constant, got {str(self.token.name)}", self.line, self.char)
