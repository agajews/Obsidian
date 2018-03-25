import re
import codecs
from pprint import pformat


indent_spaces = 4


ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)


def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


def clean_string(string, to_escape):
    new_string = ''
    escaped = False
    for char in string:
        if not escaped and char == '\\':
            escaped = True
        elif escaped:
            escaped = False
            if char == to_escape:
                new_string += char
            else:
                new_string += '\\' + char
        else:
            new_string += char
    return decode_escapes(new_string)


class Node:
    def __repr__(self):
        return self.show(0)
        # return str(type(self).__name__) + pformat(self.__dict__)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


class Ident(Node):
    def __init__(self, identifier):
        self.identifier = identifier

    def show(self, indent):
        return self.identifier


class Int(Node):
    def __init__(self, val):
        #TODO: Error handling
        self.val = val

    def show(self, indent):
        return str(self.val)


class Float(Node):
    def __init__(self, val):
        #TODO: Error handling
        self.val = val

    def show(self, indent):
        return str(self.val)


class String(Node):
    def __init__(self, string):
        self.string = string

    def show(self, indent):
        return '"' + self.string.replace('"', '\\"') + '"'


class Symbol(Node):
    def __init__(self, symbol):
        self.symbol = symbol

    def show(self, indent):
        return ':' + self.symbol


class Map(Node):
    def __init__(self, elements=None):
        self.elements = elements if elements is not None else []

    def show(self, indent):
        return '{' + ', '.join(e.show(indent) for e in self.elements) + '}'


class List(Node):
    def __init__(self, elements=None):
        self.elements = elements if elements is not None else []

    def show(self, indent):
        return '[' + ', '.join(e.show(indent) for e in self.elements) + ']'


class Tuple(Node):
    def __init__(self, elements=None):
        self.elements = elements if elements is not None else []

    def show(self, indent):
        return '(' + ', '.join(e.show(indent) for e in self.elements) + ')'


class Call(Node):
    def __init__(self, callable_expr, args=None):
        self.callable_expr = callable_expr
        self.args = args if args is not None else []

    def show(self, indent):
        return '(' + self.callable_expr.show(indent) + ' ' + ' '.join(e.show(indent) for e in self.args) + ')'


# class Access(Node):
#     def __init__(self, accessable_expr, elements):
#         self.accessable_expr = accessable_expr
#         self.elements = elements

#     def show(self, indent):
#         return self.callable_expr.show(indent) + '[' + ', '.join(e.show(indent) for e in self.args) + ']'


# class CurlyAccess(Node):
#     def __init__(self, accessable_expr, elements):
#         self.accessable_expr = accessable_expr
#         self.elements = elements

#     def show(self, indent):
#         return self.callable_expr.show(indent) + '{' + ', '.join(e.show(indent) for e in self.args) + '}'


class Unary(Node):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def show(self, indent):
        return self.op + self.expr.show(indent)


class Binary(Node):
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def show(self, indent):
        return self.lhs.show(indent) + ' ' + self.op + self.rhs.show(indent)


class BinarySlurp(Node):
    def __init__(self, slurp):
        self.slurp = slurp


    def show(self, indent):
        return ' '.join(e.show(indent) for e in self.slurp)


class Block(Node):
    def __init__(self, statements):
        self.statements = statements

    def show(self, indent):
        return 'do ' + ('\n' + ' ' * (indent_spaces + 1)).join(s.show(indent + 1) for s in self.statements) + \
                '\n' + ' ' * indent_spaces + 'end'


class Semantics:
    def identifier(identifier):
        return Ident(identifier)

    def binary_identifier(identifier):
        return Ident(identifier)

    def op(op):
        return Ident(op)

    def integer(int_str):
        return Int(int(int_str))

    def float(float_str):
        return Float(float(float_str))

    def double_string(string):
        return String(clean_string(string[1:-1], '"'))

    def single_string(string):
        return String(clean_string(string[1:-1], "'"))

    def symbol(symbol):
        return Symbol(symbol)

    def tuple(info):
        if info.get('first') is None:
            return Tuple()
        return Tuple([info['first']] + info['rest'])

    def map(info):
        if info.get('first') is None:
            return Map()
        return Map([info['first']] + info['rest'])

    def list(elements):
        return List(elements)

    def unary_expression(info):
        return Unary(info['op'], info['expression'])

    def binary_slurp(slurp):
        if len(slurp) == 1:
            return slurp[0]
        return BinarySlurp(slurp)

    def block_binary_expression(info):
        return Binary(info['op'], info['lhs'], info['rhs'])

    def block(statements):
        return Block([s for s in statements if s != '\n'])

    def statement(info):
        if len(info['args']) == 0:
            return info['head']
        return Call(info['head'], info['args'])

    def call_expression(info):
        return Call(info['head'], info['args'])

    def partial_call_expression(info):
        if len(info['args']) == 0:
            return info['head']
        return Call(info['head'], info['args'])

    # def program(statements):
    #     return [s for s in statements if s != '\n']

    # def newlines(info):
    #     return '\n'

    # def semicolons(info):
    #     return '\n'

    def statement_list(info):
        statements = []
        if info.get('first') is not None:
            statements.append(info['first'])
        statements += info['rest']
        return statements
