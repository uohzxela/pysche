import sys
import io
import pdb


class IO(object):
    reader = None

    @staticmethod
    def initialize_reader(stream):
        IO.reader = io.open(stream.fileno(), mode='rb')

    @staticmethod
    def peek():
        return IO.reader.peek(1)[0]

    @staticmethod
    def getc():
        return IO.reader.read(1)

    @staticmethod
    def prompt():
        sys.stdout.write("> ")
        sys.stdout.flush()


class Token(object):
    LPAREN = '('
    RPAREN = ')'
    SPACE = ' '
    CR = '\r'
    LF = '\n'
    TAB = '\t'


class Type(object):
    FIXNUM = 1
    SYMBOL = 2
    LIST = 3


class Fixnum(object):
    def __init__(self, val):
        self.type = Type.FIXNUM
        self.val = val

    def __str__(self):
        return str(self.val)


class Symbol(object):
    def __init__(self, val):
        self.type = Type.SYMBOL
        self.val = val

    def __str__(self):
        return "\"" + self.val + "\""


class List(object):
    def __init__(self, list):
        self.type = Type.LIST
        self.list = list

    def __str__(self):
        buffer = []
        for obj in self.list:
            buffer.append(str(obj))
        return "(" + ", ".join(buffer) + ")"


def read_list():
    L = []
    while True:
        expr = read_expr()
        if expr == Token.RPAREN:
            return L
        L.append(expr)


def read_fixnum(num):
    while IO.peek().isdigit():
        num = num * 10 + int(IO.getc())
    return num


def read_symbol(c):
    buffer = [c]
    while IO.peek().isalpha():
        buffer.append(IO.getc())
    return ''.join(buffer)


def is_redundant(c):
    return (c == Token.SPACE or
            c == Token.LF or
            c == Token.CR or
            c == Token.TAB)


def read_expr():
    c = IO.getc()
    # skip whitespaces, newlines or tabs
    if is_redundant(c):
        return read_expr()
    elif c == Token.LPAREN:
        return List(read_list())
    elif c == Token.RPAREN:
        return Token.RPAREN
    elif c.isalpha():
        # TODO: intern symbol
        return Symbol(read_symbol(c))
    elif c.isdigit():
        return Fixnum(read_fixnum(int(c)))
    elif c == '-' and IO.peek().isdigit():
        return Fixnum(-1*read_fixnum(int(IO.getc())))
    elif c == '':  # EOF
        return None
    return read_expr()


def main():
    if len(sys.argv) == 1:
        print "Welcome to scheme.py. Use ctrl-c to exit."
        stream = sys.stdin
    else:
        stream = open(sys.argv[1])
    IO.initialize_reader(stream)

    try:
        while True:
            IO.prompt()
            expr = read_expr()
            if expr is None:
                break
            print expr
    except KeyboardInterrupt:
        print "\nGoodbye."

if __name__ == "__main__":
    main()
