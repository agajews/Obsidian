import re
import codecs


indent_spaces = 4


# ESCAPE_SEQUENCE_RE = re.compile(r'''
#     ( \\U........      # 8-digit hex escapes
#     | \\u....          # 4-digit hex escapes
#     | \\x..            # 2-digit hex escapes
#     | \\[0-7]{1,3}     # Octal escapes
#     | \\N\{[^}]+\}     # Unicode characters by name
#     | \\[\\'"abfnrtv]  # Single-character escapes
#     )''', re.UNICODE | re.VERBOSE)
#
#
# def decode_escapes(s):
#     def decode_match(match):
#         return codecs.decode(match.group(0), 'unicode-escape')
#
#     return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


def clean_string(string, to_escape):
    new_string = ''
    escaped = False
    for char in string:
        if not escaped and char == '\\':
            escaped = True
        elif escaped:
            escaped = False
            if char in to_escape:
                new_string += char
            else:
                new_string += '\\' + char
        else:
            new_string += char
    # return decode_escapes(new_string)
    return new_string


class Node:
    def __repr__(self):
        # return self.show(0)
        return str(type(self).__name__) + str(self.__dict__)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


class Ident(Node):
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return 'Ident({})'.format(self.identifier)

    def show(self, indent):
        return self.identifier


class Int(Node):
    def __init__(self, val, sigil=None):
        # TODO: Error handling
        self.val = val
        self.sigil = sigil

    def show(self, indent):
        return str(self.val)


class Float(Node):
    def __init__(self, val, sigil=None):
        # TODO: Error handling
        self.val = val
        self.sigil = sigil

    def show(self, indent):
        return str(self.val)


class String(Node):
    def __init__(self, string, sigil=None):
        self.string = string
        self.sigil = sigil

    def show(self, indent):
        return '"' + self.string.replace('"', '\\"') + '"'


class InterpolatedString(Node):
    def __init__(self, body, sigil=None):
        self.body = body
        self.sigil = sigil

    def show(self, indent):
        return '"' + ''.join(b.show(indent) for b in self.body) + '"'


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


class Trailed(Node):
    def __init__(self, expr, trailers=None):
        self.expr = expr
        self.trailers = trailers if trailers is not None else []

# class PartialCall(Node):
#     def __init__(self, callable_expr, args=None):
#         self.callable_expr = callable_expr
#         self.args = args if args is not None else []
#
#     def show(self, indent):
#         return '[' + self.callable_expr.show(indent) + ' ' + ' '.join(e.show(indent) for e in self.args) + ']'


class Unquote(Node):
    def __init__(self, expr):
        self.expr = expr

    def show(self, indent):
        return '$' + self.expr.show(indent)


# class Binary(Node):
#     def __init__(self, op, lhs, rhs):
#         self.op = op
#         self.lhs = lhs
#         self.rhs = rhs
#
#     def show(self, indent):
#         return self.lhs.show(indent) + ' ' + self.op + self.rhs.show(indent)
#

class BinarySlurp(Node):
    def __init__(self, slurp):
        self.slurp = slurp

    def show(self, indent):
        return ' '.join(e.show(indent) for e in self.slurp)


class Block(Node):
    def __init__(self, statements):
        self.statements = statements

    def show(self, indent):
        return '{' + ('\n' + ' ' * (indent_spaces + 1)).join(s.show(indent + 1) for s in self.statements) + \
            '\n' + ' ' * indent_spaces + '}'


class Semantics:
    def identifier(identifier):
        return Ident(identifier)

    def binary_identifier(identifier):
        return Ident(identifier)

    def op(op):
        return Ident(op)

    def integer(info):
        return Int(int(float(info['val'].replace('_', ''))), info['sigil'])

    def float(info):
        return Float(float(info['val'].replace('_', '')), info['sigil'])

    def interpolated_string(info):
        bodies = info['bodies']
        sigil = info['sigil']
        if len(bodies) == 0:
            return String('', sigil)
        if len(bodies) == 1 and isinstance(bodies[0], String):
            return String(bodies[0].string, sigil)
        return InterpolatedString(bodies, sigil)

    def triple_interpolated_string(info):
        bodies = info['bodies']
        sigil = info['sigil']
        if len(bodies) == 0:
            return String('', sigil)
        if len(bodies) == 1 and isinstance(bodies[0], String):
            return String(bodies[0].string, sigil)
        return InterpolatedString(bodies, sigil)

    def STRING_BODY(body):
        return String(clean_string(body, '"$'))

    def TSTRING_BODY(body):
        return String(clean_string(body, '"$'))

    def single_string(info):
        return String(clean_string(info['val'][1:-1], "'"), info['sigil'])

    # def triple_double_string(info):
    #     return String(clean_string(info['val'][3:-3], '"'), info['sigil'])
    #
    def triple_single_string(info):
        return String(clean_string(info['val'][3:-3], "'"), info['sigil'])

    def symbol(symbol):
        return Symbol(symbol)

    def tuple(info):
        if info.get('first') is None:
            return Tuple()
        rest = info['rest'] if info['rest'] is not None else []
        return Tuple([info['first']] + rest)

    def map(info):
        if info.get('first') is None:
            return Map()
        rest = info['rest'] if info['rest'] is not None else []
        return Map([info['first']] + rest)

    def list(contents):
        if contents is None:
            return List()
        return List(contents)

    def simple_expression(info):
        if len(info['trailers']) == 0:
            return info['expr']
        return Trailed(info['expr'], info['trailers'])

    def simple_single_expression(info):
        if len(info['trailers']) == 0:
            return info['expr']
        return Trailed(info['expr'], info['trailers'])

    def binary_slurp(slurp):
        if len(slurp) == 1:
            return slurp[0]
        return BinarySlurp(slurp)

    def block_slurp(slurp):
        if len(slurp) == 1:
            return slurp[0]
        return BinarySlurp(slurp)

    # def block_binary_expression(info):
    #     return Binary(info['op'], info['lhs'], info['rhs'])
    #
    def block(statements):
        return Block([s for s in statements if s != '\n'])

    def statement(info):
        if len(info['args']) == 0:
            return info['head']
        return Call(info['head'], info['args'])

    def call_expression(info):
        return Call(info['head'], info['args'])

    def partial_call_expression(info):
        return PartialCall(info['head'], info['args'])

    def unquote_expression(info):
        return Unquote(info)

    def curly_expression(exprs):
        if len(exprs) == 1:
            return exprs[0]
        return Block(exprs)

    def statement_list(info):
        statements = []
        if info.get('first') is not None:
            statements.append(info['first'])
        statements += info['rest']
        return statements
