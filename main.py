import sys
import lex
import parse
import eval
import ps_error

def main():
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        lexer = lex.Lexer()
        tokens = lexer.lexer(lines)
#        print(tokens)
        parser = parse.Parser(tokens)
        ast = parser.parse()
#        print(ast)
        if isinstance(ast, ps_error.PS_Error):
            sys.tracebacklimit = 0
            ast.add_ctx(lines)
            print(ast.message)
            return
        else:
            bytecode = ast.compile()
            if isinstance(bytecode, ps_error.PS_Error):
                sys.tracebacklimit = 0
                bytecode.add_ctx(lines)
                print(bytecode.message)
                return
#            print(bytecode)
            eval.eval(bytecode)

if __name__ == "__main__":
    main()
