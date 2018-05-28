from ..bootstrap import (
    Panic,
    Object,
    Type,
    PrimFun,
    String,
    object_type,
)
from .int import Int
from .bool import true, false


class Symbol(Object):
    def __init__(self, symbol):
        super().__init__({}, symbol_type)
        self.symbol = symbol

    def __repr__(self):
        return '@{}'.format(self.symbol)


class SymbolHash(PrimFun):
    def __init__(self):
        super().__init__('Symbol.hash', ['symbol'])

    def fun(self, symbol):
        if not isinstance(symbol, Symbol):
            raise Panic('Argument must be a symbol')
        return Int(hash(symbol.symbol))


class SymbolEq(PrimFun):
    def __init__(self):
        super().__init__('Symbol.eq', ['a', 'b'])

    def fun(self, a, b):
        if not isinstance(a, Symbol):
            raise Panic('Argument `a` must be a symbol')
        if not isinstance(b, Symbol):
            raise Panic('Argument `b` must be a symbol')
        return true if a.symbol == b.symbol else false


class SymbolToStr(PrimFun):
    def __init__(self):
        super().__init__('Symbol.to_str', ['symbol'])

    def fun(self, symbol):
        if not isinstance(symbol, Symbol):
            raise Panic('Argument must be a symbol')
        return String('@{}'.format(symbol.symbol))


class SymbolConstructor(PrimFun):
    def __init__(self):
        super().__init__('Symbol', ['ast'])

    def macro(self, scope, ast):
        symbol = ast.get('symbol')
        if not isinstance(symbol, Symbol):
            raise Panic('Invalid symbol')
        return Symbol(symbol.symbol)


class SymbolType(Type):
    def __init__(self):
        super().__init__('Symbol', object_type,
                         methods={'to_str': SymbolToStr()},
                         constructor=SymbolConstructor())


symbol_type = SymbolType()
symbol_type.get('methods').set('eq', SymbolEq())
symbol_type.get('methods').set('hash', SymbolHash())
