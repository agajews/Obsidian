from ..types import (
    PrimFun,
    String,
    Symbol,
    Int,
    true,
    false,
)
from ..types.ast import ASTSymbol


class SymbolHash(PrimFun):
    def __init__(self):
        super().__init__('Symbol.hash', ['symbol'])

    def fun(self, symbol):
        self.typecheck_arg(symbol, Symbol)
        return Int(hash(symbol.symbol))


class SymbolEq(PrimFun):
    def __init__(self):
        super().__init__('Symbol.eq', ['a', 'b'])

    def fun(self, a, b):
        self.typecheck_arg(a, Symbol)
        self.typecheck_arg(b, Symbol)
        return true if a.symbol == b.symbol else false


class SymbolToStr(PrimFun):
    def __init__(self):
        super().__init__('Symbol.to_str', ['symbol'])

    def fun(self, symbol):
        self.typecheck_arg(symbol, Symbol)
        return String('@{}'.format(symbol.symbol))


class SymbolConstructor(PrimFun):
    def __init__(self):
        super().__init__('Symbol', ['ast'])

    def macro(self, scope, ast):
        self.typecheck_arg(ast, ASTSymbol)
        ast.validate()
        return Symbol(ast.get('symbol').symbol)


Symbol.T.get('methods').set('eq', SymbolEq())
Symbol.T.get('methods').set('hash', SymbolHash())
Symbol.T.get('methods').set('to_str', SymbolToStr())
Symbol.T.set('call', SymbolConstructor())
