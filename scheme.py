import sys
import io
import pdb

SYMBOL_TABLE = {}
# singleton boolean objects
false = None
true = None


class IO(object):
    reader = None

    @staticmethod
    def init_reader(stream):
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
    RETURN = '\r'
    NEWLINE = '\n'
    TAB = '\t'
    HASH = '#'
    DOUBLE_QUOTE = '\"'
    BACKSLASH = '\\'


class Type(object):
    FIXNUM = 1
    SYMBOL = 2
    LIST = 3
    BOOLEAN = 4
    CHARACTER = 5


class Character(object):
    def __init__(self, val):
        self.type = Type.CHARACTER
        self.val = val

    def __str__(self):
        c = self.val
        prefix = "#\\"
        if c == Token.NEWLINE:
            return prefix + "newline"
        elif c == Token.TAB:
            return prefix + "tab"
        elif c == Token.SPACE:
            return prefix + "space"
        else:
            return prefix + c


class Boolean(object):
    def __init__(self, val):
        self.type = Type.BOOLEAN
        self.val = val

    def __str__(self):
        return "#f" if self.val == 0 else "#t"


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
        buffer = [Token.DOUBLE_QUOTE]
        # escape during printing
        for c in self.val:
            if c == Token.NEWLINE:
                c = '\\n'
            elif c == Token.TAB:
                c = '\\t'
            elif c == Token.DOUBLE_QUOTE:
                c = '\\"'
            elif c == Token.BACKSLASH:
                c = '\\\\'
            buffer.append(c)
        buffer.append(Token.DOUBLE_QUOTE)
        return "".join(buffer)


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


def read_char():
    buffer = []
    while IO.peek().isalnum():
        buffer.append(IO.getc())
    char = "".join(buffer)
    if buffer:
        if char == "newline":
            return Character(Token.NEWLINE)
        elif char == "space":
            return Character(Token.SPACE)
        elif char == "tab":
            return Character(Token.TAB)
        elif len(char) == 1:
            return Character(char)
    else:
        if IO.peek() == ' ':
            return Character(Token.SPACE)
        elif IO.peek() == Token.NEWLINE:
            return Character(Token.NEWLINE)
        elif IO.peek() == Token.TAB:
            return Character(Token.TAB)
    raise ValueError("unknown character literal")


def read_bool_or_char():
    c = IO.getc()
    if c == 't':
        return true
    elif c == 'f':
        return false
    elif c == Token.BACKSLASH:
        return read_char()
    raise ValueError("unknown boolean literal")


def read_symbol():
    buffer = []
    while IO.peek() != Token.DOUBLE_QUOTE:
        c = IO.getc()
        # unescape
        if c == Token.BACKSLASH:
            next_c = IO.getc()
            if next_c == Token.DOUBLE_QUOTE:
                c = Token.DOUBLE_QUOTE
            elif next_c == 'n':
                c = Token.NEWLINE
            elif next_c == 't':
                c = Token.TAB
            elif next_c == Token.BACKSLASH:
                c = Token.BACKSLASH
            else:
                c += next_c
        buffer.append(c)
    IO.getc()  # get rid of double quote
    return "".join(buffer)


def intern_symbol(sym):
    if sym not in SYMBOL_TABLE:
        SYMBOL_TABLE[sym] = Symbol(sym)
    return SYMBOL_TABLE[sym]


def is_redundant(c):
    return (c == Token.SPACE or
            c == Token.NEWLINE or
            c == Token.RETURN or
            c == Token.TAB)


def read_expr():
    try:
        c = IO.getc()
        # skip whitespaces, newlines or tabs
        if is_redundant(c):
            return read_expr()
        elif c == Token.LPAREN:
            return List(read_list())
        elif c == Token.RPAREN:
            return Token.RPAREN
        elif c == Token.HASH:
            return read_bool_or_char()
        elif c == Token.DOUBLE_QUOTE:
            return intern_symbol(read_symbol())
        elif c.isdigit():
            return Fixnum(read_fixnum(int(c)))
        elif c == '-' and IO.peek().isdigit():
            return Fixnum(-1*read_fixnum(int(IO.getc())))
        elif c == '':  # EOF
            return None
        return read_expr()
    except ValueError as e:
        return e


def eval(expr):
    return expr


def init():
    global false, true
    false = Boolean(0)
    true = Boolean(1)


def main():
    if len(sys.argv) == 1:
        print "Welcome to scheme.py. Use ctrl-c to exit."
        stream = sys.stdin
    else:
        stream = open(sys.argv[1])
    IO.init_reader(stream)
    init()
    try:
        while True:
            IO.prompt()
            expr = read_expr()
            if expr is None:
                break
            print eval(expr)
    except KeyboardInterrupt:
        print "\nGoodbye."

if __name__ == "__main__":
    main()
