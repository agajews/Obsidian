from ..types import (
    PrimFun,
    Panic,
    String,
    Map,
    string_type,
    Int,
    true,
    false,
)
from ..types.ast import ASTString
# from .map import DummyKey
from .get_attr import get_attr


class StringConstructor(PrimFun):
    def __init__(self):
        super().__init__('String', ['ast'])

    def macro(self, scope, ast):
        string = ast.get('str')
        if not isinstance(string, String):
            raise Panic('Invalid string')
        sigil = ast.get('sigil')
        if not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        if sigil.str == '':
            return string
        constructors = string_type.get('sigils')
        constructor = get_attr.fun(
            constructors, String('get')).call(scope, [ASTString(sigil)])
        return constructor.call(scope, [ASTString(string)])


class StringDefaultConstructor(PrimFun):
    def __init__(self):
        super().__init__('String', ['string'])

    def fun(self, string):
        return string


class StringHash(PrimFun):
    def __init__(self):
        super().__init__('String.hash', ['string'])

    def fun(self, string):
        if not isinstance(string, String):
            raise Panic('Argument must be a string')
        return Int(hash(string.str))


class StringEq(PrimFun):
    def __init__(self):
        super().__init__('String.eq', ['a', 'b'])

    def fun(self, a, b):
        if not isinstance(a, String):
            raise Panic('Argument `a` must be a string')
        if not isinstance(b, String):
            raise Panic('Argument `b` must be a string')
        return true if a.str == b.str else false


class Concat(PrimFun):
    def __init__(self):
        super().__init__('String.get', variadic=True)

    def fun(self, *strings):
        catted_string = ''
        for string in strings:
            if not isinstance(string, String):
                raise Panic('Strings must be strings')
            catted_string += string.str
        return String(catted_string)


string_type.set('call', StringConstructor())
string_type.set('sigils', Map({
    # DummyKey(String(''), ''): StringDefaultConstructor(),
}))
string_type.get('methods').set('hash', StringHash())
string_type.get('methods').set('eq', StringEq())
concat = Concat()
