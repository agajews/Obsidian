from ... import semantics as sem
from ..bootstrap import (
    String,
    Object, Type, Panic,
    object_type,
    nil
)
from .int import Int
from .float import Float
from .list import List
from .symbol import Symbol


class ASTNodeType(Type):
    def __init__(self):
        super().__init__('Node', object_type, [])


class ASTIdent(Object):
    def __init__(self, ident):
        if not isinstance(ident, String):
            raise Panic('Invalid ident')
        super().__init__({'ident': ident}, ast_ident_type)

    def __repr__(self):
        return 'ASTIdent({})'.format(self.get('ident'))


class ASTIdentType(Type):
    def __init__(self):
        super().__init__('Ident', ast_node_type, ['ident'])

    def fun(self, ident):
        return ASTIdent(ident)


class ASTString(Object):
    def __init__(self, string, sigil=None):
        if not isinstance(string, String):
            raise Panic('Invalid string')
        if sigil is not nil and not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        super().__init__(
            {'str': string, 'sigil': nil if sigil is None else sigil}, ast_string_type)

    def __repr__(self):
        return 'ASTString({}, {})'.format(self.get('str'), self.get('sigil'))


class ASTStringType(Type):
    def __init__(self):
        super().__init__('String', ast_node_type, ['str', 'sigil'])

    def fun(self, string, sigil):
        return ASTString(string, sigil)


class ASTInt(Object):
    def __init__(self, val, sigil=None):
        if not isinstance(val, Int):
            raise Panic('Invalid int')
        if sigil is not nil and not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        super().__init__(
            {'int': val, 'sigil': nil if sigil is None else sigil}, ast_int_type)

    def __repr__(self):
        return 'ASTInt({}, {})'.format(self.get('int'), self.get('sigil'))


class ASTIntType(Type):
    def __init__(self):
        super().__init__('Int', ast_node_type, ['int', 'sigil'])

    def fun(self, val, sigil):
        return ASTInt(val, sigil)


class ASTFloat(Object):
    def __init__(self, val, sigil=None):
        if not isinstance(val, Float):
            raise Panic('Invalid float')
        if sigil is not nil and not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        super().__init__(
            {'float': val, 'sigil': nil if sigil is None else sigil}, ast_float_type)

    def __repr__(self):
        return 'ASTFloat({}, {})'.format(self.get('float'), self.get('sigil'))


class ASTFloatType(Type):
    def __init__(self):
        super().__init__('Float', ast_node_type, ['float', 'sigil'])

    def fun(self, val, sigil):
        return ASTFloat(val, sigil)


class ASTSymbol(Object):
    def __init__(self, symbol):
        if not isinstance(symbol, Symbol):
            raise Panic('Invalid symbol')
        super().__init__(
            {'symbol': symbol}, ast_symbol_type)

    def __repr__(self):
        return 'ASTSymbol({})'.format(self.get('symbol'))


class ASTSymbolType(Type):
    def __init__(self):
        super().__init__('Symbol', ast_node_type, ['symbol'])

    def fun(self, symbol):
        return ASTSymbol(symbol)


class ASTList(Object):
    def __init__(self, elems):
        if not isinstance(elems, List):
            raise Panic('Invalid list')
        super().__init__({'elems': elems}, ast_list_type)

    def __repr__(self):
        return 'ASTList({})'.format(self.get('elems'))


class ASTListType(Type):
    def __init__(self):
        super().__init__('List', ast_node_type, ['list'])

    def fun(self, lst):
        return ASTList(lst)


class ASTCall(Object):
    def __init__(self, callable_expr, args):
        super().__init__(
            {'callable': callable_expr, 'args': args}, ast_call_type)

    def __repr__(self):
        return 'ASTCall({}, {})'.format(self.get('callable'), self.get('args'))


class ASTCallType(Type):
    def __init__(self):
        super().__init__('Call', ast_node_type, ['callable', 'args'])

    def fun(self, callable_expr, args):
        return ASTCall(callable_expr, args)


class ASTBinarySlurp(Object):
    def __init__(self, slurp):
        if not isinstance(slurp, List):
            raise Panic('Invalid slurp')
        super().__init__({'slurp': slurp}, ast_binary_slurp_type)

    def __repr__(self):
        return ' '.join(str(e) for e in self.get('slurp').elems)


class ASTBinarySlurpType(Type):
    def __init__(self):
        super().__init__('BinarySlurp', ast_node_type, ['slurp'])

    def fun(self, slurp):
        return ASTBinarySlurp(slurp)


def model_to_ast(model):
    if isinstance(model, sem.Ident):
        return ASTIdent(String(model.identifier))
    elif isinstance(model, sem.Call):
        return ASTCall(model_to_ast(model.callable_expr), List([model_to_ast(arg) for arg in model.args]))
    elif isinstance(model, sem.String):
        return ASTString(String(model.string), String(model.sigil) if model.sigil is not None else nil)
    elif isinstance(model, sem.Int):
        return ASTInt(Int(model.val), String(model.sigil) if model.sigil is not None else nil)
    elif isinstance(model, sem.Float):
        return ASTFloat(Float(model.val), String(model.sigil) if model.sigil is not None else nil)
    elif isinstance(model, sem.List):
        return ASTList(List([model_to_ast(elem) for elem in model.elements]))
    elif isinstance(model, sem.Symbol):
        return ASTSymbol(Symbol(model.symbol))
    elif isinstance(model, sem.BinarySlurp):
        return ASTBinarySlurp(List([model_to_ast(elem) for elem in model.slurp]))
    else:
        raise NotImplementedError(
            'Translation of model node {} to AST not implemented'.format(model))


ast_node_type = ASTNodeType()
ast_ident_type = ASTIdentType()
ast_string_type = ASTStringType()
ast_int_type = ASTIntType()
ast_float_type = ASTFloatType()
# ASTInterpolatedStringType = Type('InterpolatedString', ASTNodeType)
ast_symbol_type = ASTSymbolType()
ast_list_type = ASTListType()
# ASTMapType = Type('Map', ASTNodeType)
# ASTTupleType = Type('Tuple', ASTNodeType)
ast_call_type = ASTCallType()
# ASTPartialCallType = Type('PartialCall', ASTNodeType)
# ASTUnquoteType = Type('Unquote', ASTNodeType)
ast_binary_slurp_type = ASTBinarySlurpType()
# ASTBlockType = Type('Block', ASTNodeType)
