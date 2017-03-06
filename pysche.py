import sys
import io
import pdb

LPAREN = '('
RPAREN = ')'
# initialize a global file reader 
# to avoid passing it around as function arg
reader = None

def read_list():
    L = []
    while True:
        expr = read_expr()
        if expr == RPAREN:
            return L
        L.append(expr)


def peek():
    return reader.peek(1)


def getc():
    return reader.read(1)


def read_number(num):
    while peek().isdigit():
        num = num * 10 + int(getc())
    return num


def read_symbol(c):
    buffer = [c]
    while peek().isalpha():
        buffer.append(getc())
    # TODO: intern symbol
    return ''.join(buffer)


def is_redundant(c):
    return (c == ' ' or c == '\n' or c == '\r' or c == '\t')


def read_expr():
    c = getc()
    # skip whitespaces, newlines or tabs
    if is_redundant(c):
        return read_expr()
    elif c == LPAREN:
        return read_list()
    elif c == RPAREN:
        return RPAREN
    elif c.isalpha():
        return read_symbol(c)
    elif c.isdigit():
        return read_number(int(c))
    elif not c: # EOF
        return None
    return read_expr()


def main():
    if len(sys.argv) == 1:
        print "Welcome to Pysche. Use ctrl-c to exit."
        stream = sys.stdin
    else:
        stream = open(sys.argv[1])

    global reader
    reader = io.open(stream.fileno(), mode='rb', closefd=False)

    try:
        while True:
            expr = read_expr()
            if not expr: # EOF
                break
            print ">",
            print expr
    except KeyboardInterrupt:
        print "\nGoodbye."

if __name__ == "__main__":
    main()
