from ..bootstrap import (
    Panic,
    Object,
    Type,
    PrimFun,
    String,
    object_type,
)


class Symbol(Object):
    def __init__(self, symbol):
        super().__init__({}, symbol_type)
        self.symbol = symbol

    def __repr__(self):
        return '@{}'.format(self.symbol)


class SymbolToStr(PrimFun):
    def __init__(self):
        super().__init__('to_str', ['symbol'])

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
