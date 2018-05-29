indent_spaces = 4


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
    def __init__(self, parseinfo=None):
        self.parseinfo = parseinfo

    def __repr__(self):
        # return self.show(0)
        return str(type(self).__name__) + str(self.__dict__)

    def __eq__(self, other):
        def clean_dict(dictionary):
            {k: v for k, v in dictionary.items() if k != 'parseinfo'}
        if type(other) is type(self):
            return clean_dict(self.__dict__) == clean_dict(other.__dict__)
        return False


class Ident(Node):
    def __init__(self, identifier, parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.identifier = identifier

    def __repr__(self):
        return 'Ident({})'.format(self.identifier)

    def show(self, indent):
        return self.identifier


class Int(Node):
    def __init__(self, val, sigil='', parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        # TODO: Error handling
        self.val = val
        self.sigil = sigil

    def show(self, indent):
        return str(self.val)


class Float(Node):
    def __init__(self, val, sigil='', parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        # TODO: Error handling
        self.val = val
        self.sigil = sigil

    def show(self, indent):
        return str(self.val)


class String(Node):
    def __init__(self, string, sigil='', parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.string = string
        self.sigil = sigil

    def show(self, indent):
        return '"' + self.string.replace('"', '\\"') + '"'


class StringBody(Node):
    def __init__(self, string, parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.string = string


class InterpolatedString(Node):
    def __init__(self, body, parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.body = body

    def show(self, indent):
        return '"' + ''.join(b.show(indent) for b in self.body) + '"'


class Symbol(Node):
    def __init__(self, symbol, parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.symbol = symbol

    def show(self, indent):
        return ':' + self.symbol


class Map(Node):
    def __init__(self, elements=None, parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.elements = elements if elements is not None else []

    def show(self, indent):
        return '{' + ', '.join(e.show(indent) for e in self.elements) + '}'


class List(Node):
    def __init__(self, elements=None, parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.elements = elements if elements is not None else []

    def show(self, indent):
        return '[' + ', '.join(e.show(indent) for e in self.elements) + ']'


class Tuple(Node):
    def __init__(self, elements=None, parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.elements = elements if elements is not None else []

    def show(self, indent):
        return '(' + ', '.join(e.show(indent) for e in self.elements) + ')'


class Call(Node):
    def __init__(self, callable_expr, args=None, parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.callable_expr = callable_expr
        self.args = args if args is not None else []

    def show(self, indent):
        return '(' + self.callable_expr.show(indent) + ' ' + ' '.join(e.show(indent) for e in self.args) + ')'


class Unquote(Node):
    def __init__(self, expr, parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.expr = expr

    def show(self, indent):
        return '$' + self.expr.show(indent)


class BinarySlurp(Node):
    def __init__(self, slurp, parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.slurp = slurp

    def show(self, indent):
        return ' '.join(e.show(indent) for e in self.slurp)


class Block(Node):
    def __init__(self, statements, parseinfo=None):
        super().__init__(parseinfo=parseinfo)
        self.statements = statements

    def show(self, indent):
        return '{' + ('\n' + ' ' * (indent_spaces + 1)).join(s.show(indent + 1) for s in self.statements) + \
            '\n' + ' ' * indent_spaces + '}'


class Semantics:
    def identifier(info):
        return Ident(info['ident'], parseinfo=info.parseinfo)

    def binary_identifier(info):
        return Ident(info['ident'], parseinfo=info.parseinfo)

    def op(info):
        return Ident(info['op'], parseinfo=info.parseinfo)

    def integer(info):
        sigil = '' if info['sigil'] is None else info['sigil']
        return Int(int(float(info['val'].replace('_', ''))), sigil, parseinfo=info.parseinfo)

    def float(info):
        sigil = '' if info['sigil'] is None else info['sigil']
        return Float(float(info['val'].replace('_', '')), sigil, parseinfo=info.parseinfo)

    def interpolated_string(info):
        bodies = info['bodies']
        sigil = '' if info['sigil'] is None else info['sigil']
        if len(bodies) == 0:
            return String('', sigil, parseinfo=info.parseinfo)
        if len(bodies) == 1 and isinstance(bodies[0], StringBody):
            return String(bodies[0].string, sigil, parseinfo=info.parseinfo)
        bodies = [String(body.string, sigil, parseinfo=body.parseinfo)
                  if isinstance(body, StringBody) else body
                  for body in bodies]
        return InterpolatedString(bodies, parseinfo=info.parseinfo)

    def triple_interpolated_string(info):
        bodies = info['bodies']
        sigil = '' if info['sigil'] is None else info['sigil']
        if len(bodies) == 0:
            return String('', sigil, parseinfo=info.parseinfo)
        if len(bodies) == 1 and isinstance(bodies[0], StringBody):
            return String(bodies[0].string, sigil, parseinfo=info.parseinfo)
        bodies = [String(body.string, sigil, parseinfo=body.parseinfo)
                  if isinstance(body, StringBody) else body
                  for body in bodies]
        return InterpolatedString(bodies, parseinfo=info.parseinfo)

    def STRING_BODY(info):
        return StringBody(clean_string(info['body'], '"$'), parseinfo=info.parseinfo)

    def TSTRING_BODY(info):
        return StringBody(clean_string(info['body'], '"$'), parseinfo=info.parseinfo)

    def single_string(info):
        sigil = '' if info['sigil'] is None else info['sigil']
        return String(clean_string(info['val'][1: -1], "'"), sigil, parseinfo=info.parseinfo)

    def triple_single_string(info):
        sigil = '' if info['sigil'] is None else info['sigil']
        return String(clean_string(info['val'][3: -3], "'"), sigil, parseinfo=info.parseinfo)

    def symbol(info):
        return Symbol(info['symbol'], parseinfo=info.parseinfo)

    def tuple(info):
        if info.get('first') is None:
            return Tuple()
        rest = info['rest'] if info['rest'] is not None else []
        return Tuple([info['first']] + rest, parseinfo=info.parseinfo)

    def map(info):
        if info.get('first') is None:
            return Map()
        rest = info['rest'] if info['rest'] is not None else []
        return Map([info['first']] + rest, parseinfo=info.parseinfo)

    def list(info):
        if info['contents'] is None:
            return List()
        return List(info['contents'], parseinfo=info.parseinfo)

    def binary_slurp(info):
        slurp = info['slurp']
        if len(slurp) == 1:
            return slurp[0]
        return BinarySlurp(slurp, parseinfo=info.parseinfo)

    def block_slurp(info):
        slurp = info['slurp']
        if len(slurp) == 1:
            return slurp[0]
        return BinarySlurp(slurp, parseinfo=info.parseinfo)

    def block(info):
        return Block([s for s in info['statements'] if s != '\n'], parseinfo=info.parseinfo)

    def statement(info):
        if len(info['args']) == 0:
            return info['head']
        return Call(info['head'], info['args'], parseinfo=info.parseinfo)

    def call_expression(info):
        return Call(info['head'], info['args'], parseinfo=info.parseinfo)

    def unquote_expression(info):
        return Unquote(info, parseinfo=info.parseinfo)

    def curly_expression(info):
        exprs = info['exprs']
        if len(exprs) == 1:
            return exprs[0]
        return Block(exprs, parseinfo=info.parseinfo)

    def statement_list(info):
        statements = []
        if info.get('first') is not None:
            statements.append(info['first'])
        statements += info['rest']
        return statements
