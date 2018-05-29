from ... import semantics as sem
from ..bootstrap import (
    PrimFun,
    String,
    Object,
    Type,
    Panic,
    object_type,
)
from .int import Int
from .float import Float
from .list import List
from .tuple import Tuple
from .symbol import Symbol


class ASTNodeType(Type):
    def __init__(self):
        super().__init__('ast.Node', object_type)


class ASTString(Object):
    def __init__(self, string, sigil=None, parseinfo=None):
        if not isinstance(string, String):
            raise Panic('Invalid string')
        if sigil is None:
            sigil = String('')
        if not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        self.parseinfo = parseinfo
        super().__init__(
            {'str': string, 'sigil': sigil}, ast_string_type)

    def __repr__(self):
        return 'ASTString({}, {})'.format(self.get('str'), self.get('sigil'))


class ASTStringConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.String', ['str', 'sigil'])

    def fun(self, string, sigil):
        return ASTString(string, sigil)


class ASTStringType(Type):
    def __init__(self):
        super().__init__('ast.String', ast_node_type, constructor=ASTStringConstructor())


class ASTInterpolatedString(Object):
    def __init__(self, body, parseinfo=None):
        if not isinstance(body, List):
            raise Panic('Body must be a list')
        self.parseinfo = parseinfo
        super().__init__(
            {'body': body}, ast_interpolated_string_type)

    def body_list(self):
        body = self.get('body')
        if not isinstance(body, List):
            raise Panic('`ast.InterpolatedString` body must be a `List`')
        return body.elems

    def __repr__(self):
        return 'ASTInterpolatedString({})'.format(self.get('body'))


class ASTInterpolatedStringConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.InterpolatedString', ['body'])

    def fun(self, body):
        return ASTInterpolatedString(body)


class ASTInterpolatedStringType(Type):
    def __init__(self):
        super().__init__('ast.InterpolatedString',
                         ast_node_type, constructor=ASTInterpolatedStringConstructor())


class ASTIdent(Object):
    def __init__(self, ident, parseinfo=None):
        if not isinstance(ident, String):
            raise Panic('Invalid ident')
        self.parseinfo = parseinfo
        super().__init__({'ident': ident}, ast_ident_type)

    def __repr__(self):
        return 'ASTIdent({})'.format(self.get('ident'))


class ASTIdentConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Ident', ['ident'])

    def fun(self, ident):
        return ASTIdent(ident)


class ASTIdentType(Type):
    def __init__(self):
        super().__init__('ast.Ident', ast_node_type, constructor=ASTIdentConstructor())


class ASTInt(Object):
    def __init__(self, val, sigil=None, parseinfo=None):
        if not isinstance(val, Int):
            raise Panic('Invalid int')
        if sigil is None:
            sigil = String('')
        if not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        self.parseinfo = parseinfo
        super().__init__(
            {'int': val, 'sigil': sigil}, ast_int_type)

    def __repr__(self):
        return 'ASTInt({}, {})'.format(self.get('int'), self.get('sigil'))


class ASTIntConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Int', ['int', 'sigil'])

    def fun(self, val, sigil):
        return ASTInt(val, sigil)


class ASTIntType(Type):
    def __init__(self):
        super().__init__('ast.Int', ast_node_type, constructor=ASTIntConstructor())


class ASTFloat(Object):
    def __init__(self, val, sigil=None, parseinfo=None):
        if not isinstance(val, Float):
            raise Panic('Invalid float')
        if sigil is None:
            sigil = String('')
        if not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        self.parseinfo = parseinfo
        super().__init__(
            {'float': val, 'sigil': sigil}, ast_float_type)

    def __repr__(self):
        return 'ASTFloat({}, {})'.format(self.get('float'), self.get('sigil'))


class ASTFloatConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Float', ['float', 'sigil'])

    def fun(self, val, sigil):
        return ASTFloat(val, sigil)


class ASTFloatType(Type):
    def __init__(self):
        super().__init__('ast.Float', ast_node_type, constructor=ASTFloatConstructor())


class ASTSymbol(Object):
    def __init__(self, symbol, parseinfo=None):
        if not isinstance(symbol, Symbol):
            raise Panic('Invalid symbol')
        self.parseinfo = parseinfo
        super().__init__(
            {'symbol': symbol}, ast_symbol_type)

    def __repr__(self):
        return 'ASTSymbol({})'.format(self.get('symbol'))


class ASTSymbolConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Symbol', ['symbol'])

    def fun(self, symbol):
        return ASTSymbol(symbol)


class ASTSymbolType(Type):
    def __init__(self):
        super().__init__('ast.Symbol', ast_node_type, constructor=ASTSymbolConstructor())


class ASTList(Object):
    def __init__(self, elems, parseinfo=None):
        if not isinstance(elems, List):
            raise Panic('Invalid list')
        self.parseinfo = parseinfo
        super().__init__({'elems': elems}, ast_list_type)

    def elems_list(self):
        elems = self.get('elems')
        if not isinstance(elems, List):
            raise Panic('`ast.List` elems must be a `List`')
        return elems.elems

    def __repr__(self):
        return 'ASTList({})'.format(self.get('elems'))


class ASTListConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.List', ['list'])

    def fun(self, lst):
        return ASTList(lst)


class ASTListType(Type):
    def __init__(self):
        super().__init__('ast.List', ast_node_type, constructor=ASTListConstructor())


class ASTBlock(Object):
    def __init__(self, statements, parseinfo=None):
        if not isinstance(statements, List):
            raise Panic('Invalid list')
        self.parseinfo = parseinfo
        super().__init__({'statements': statements}, ast_block_type)

    def statements_list(self):
        statements = self.get('statements')
        if not isinstance(statements, List):
            raise Panic('`ast.Block` statements must be a `List`')
        return statements.elems

    def __repr__(self):
        return 'ASTBlock({})'.format(self.get('statements'))


class ASTBlockConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Block', ['statements'])

    def fun(self, statements):
        return ASTBlock(statements)


class ASTBlockType(Type):
    def __init__(self):
        super().__init__('ast.Block', ast_node_type, constructor=ASTBlockConstructor())


class ASTTrailed(Object):
    def __init__(self, expr, trailer, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'expr': expr, 'trailer': trailer}, ast_trailed_type)

    def __repr__(self):
        return 'ASTTrailed({}, {})'.format(self.get('expr'), self.get('trailer'))


class ASTTrailedConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Trailed', ['expr', 'trailer'])

    def fun(self, expr, trailer):
        return ASTTrailed(expr, trailer)


class ASTTrailedType(Type):
    def __init__(self):
        super().__init__('ast.Trailed', ast_node_type, constructor=ASTTrailedConstructor())


class ASTTuple(Object):
    def __init__(self, elems, parseinfo=None):
        if not isinstance(elems, Tuple):
            raise Panic('Invalid tuple')
        self.parseinfo = parseinfo
        super().__init__({'elems': elems}, ast_tuple_type)

    def elems_list(self):
        elems = self.get('elems')
        if not isinstance(elems, Tuple):
            raise Panic('`ast.Tuple` elems must be a `Tuple`')
        return elems.elems

    def __repr__(self):
        return 'ASTTuple({})'.format(self.get('elems'))


class ASTTupleConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Tuple', ['tuple'])

    def fun(self, tup):
        return ASTTuple(tup)


class ASTTupleType(Type):
    def __init__(self):
        super().__init__('ast.Tuple', ast_node_type, constructor=ASTTupleConstructor())


class ASTMap(Object):
    def __init__(self, elems, parseinfo=None):
        if not isinstance(elems, List):
            raise Panic('Invalid map')
        self.parseinfo = parseinfo
        super().__init__({'elems': elems}, ast_map_type)

    def elems_list(self):
        elems = self.get('elems')
        if not isinstance(elems, List):
            raise Panic('`ast.Map` elems must be a `List`')
        return elems.elems

    def __repr__(self):
        return 'ASTMap({})'.format(self.get('elems'))


class ASTMapConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Map', ['map'])

    def fun(self, lst):
        return ASTMap(lst)


class ASTMapType(Type):
    def __init__(self):
        super().__init__('ast.Map', ast_node_type, constructor=ASTMapConstructor())


class ASTCall(Object):
    def __init__(self, callable_expr, args, parseinfo=None):
        if not isinstance(args, List):
            raise Panic('Args must be a list')
        self.parseinfo = parseinfo
        super().__init__(
            {'callable': callable_expr, 'args': args}, ast_call_type)

    def args_list(self):
        args = self.get('args')
        if not isinstance(args, List):
            raise Panic('`ast.Call` arguments must be a `List`')
        return args.elems

    def __eq__(self, other):
        def clean_dict(dictionary):
            {k: v for k, v in dictionary.items() if k != 'parseinfo'}
        if type(other) is type(self):
            return clean_dict(self.__dict__) == clean_dict(other.__dict__)
        return False

    def __repr__(self):
        return 'ASTCall({}, {})'.format(self.get('callable'), self.get('args'))


class ASTCallConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Call', ['callable', 'args'])

    def fun(self, callable_expr, args):
        return ASTCall(callable_expr, args)


class ASTCallType(Type):
    def __init__(self):
        super().__init__('ast.Call', ast_node_type, constructor=ASTCallConstructor())


class ASTBinarySlurp(Object):
    def __init__(self, slurp, parseinfo=None):
        if not isinstance(slurp, List):
            raise Panic('Invalid slurp')
        self.parseinfo = parseinfo
        super().__init__({'slurp': slurp}, ast_binary_slurp_type)

    def __repr__(self):
        return 'ASTBinarySlurp({})'.format(' '.join(str(e) for e in self.get('slurp').elems))


class ASTBinarySlurpConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.BinarySlurp', ['slurp'])

    def fun(self, slurp):
        return ASTBinarySlurp(slurp)


class ASTBinarySlurpType(Type):
    def __init__(self):
        super().__init__('ast.BinarySlurp', ast_node_type,
                         constructor=ASTBinarySlurpConstructor())


class ASTUnquote(Object):
    def __init__(self, expr, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'expr': expr}, ast_unquote_type)

    def __repr__(self):
        return 'Unquote({})'.format(self.get('expr'))


class ASTUnquoteConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Unquote', ['expr'])

    def fun(self, expr):
        return ASTUnquote(expr)


class ASTUnquoteType(Type):
    def __init__(self):
        super().__init__('ast.Unquote', ast_node_type, constructor=ASTUnquoteConstructor())


def model_to_ast(model):
    if isinstance(model, sem.Ident):
        return ASTIdent(String(model.identifier), parseinfo=model.parseinfo)
    elif isinstance(model, sem.Call):
        return ASTCall(model_to_ast(model.callable_expr), List([model_to_ast(arg) for arg in model.args]),
                       parseinfo=model.parseinfo)
    elif isinstance(model, sem.String):
        return ASTString(String(model.string), String(model.sigil), parseinfo=model.parseinfo)
    elif isinstance(model, sem.InterpolatedString):
        return ASTInterpolatedString(List([model_to_ast(elem) for elem in model.body]),
                                     parseinfo=model.parseinfo)
    elif isinstance(model, sem.Int):
        return ASTInt(Int(model.val), String(model.sigil),
                      parseinfo=model.parseinfo)
    elif isinstance(model, sem.Float):
        return ASTFloat(Float(model.val), String(model.sigil), parseinfo=model.parseinfo)
    elif isinstance(model, sem.List):
        return ASTList(List([model_to_ast(elem) for elem in model.elements]),
                       parseinfo=model.parseinfo)
    elif isinstance(model, sem.Tuple):
        return ASTTuple(Tuple([model_to_ast(elem) for elem in model.elements]),
                        parseinfo=model.parseinfo)
    elif isinstance(model, sem.Map):
        return ASTMap(List([model_to_ast(elem) for elem in model.elements]),
                      parseinfo=model.parseinfo)
    elif isinstance(model, sem.Symbol):
        return ASTSymbol(Symbol(model.symbol),
                         parseinfo=model.parseinfo)
    elif isinstance(model, sem.BinarySlurp):
        return ASTBinarySlurp(List([model_to_ast(elem) for elem in model.slurp]),
                              parseinfo=model.parseinfo)
    elif isinstance(model, sem.Unquote):
        return ASTUnquote(model_to_ast(model.expr),
                          parseinfo=model.parseinfo)
    elif isinstance(model, sem.Block):
        return ASTBlock(List([model_to_ast(statement) for statement in model.statements]),
                        parseinfo=model.parseinfo)
    elif isinstance(model, sem.Trailed):
        expr = model_to_ast(model.expr)
        for trailer in model.trailers:
            expr = ASTTrailed(expr, model_to_ast(trailer),
                              parseinfo=model.parseinfo)
        return expr
    else:
        raise NotImplementedError(
            'Translation of model node {} to AST not implemented'.format(model))


ast_node_type = ASTNodeType()
ast_string_type = ASTStringType()
ast_interpolated_string_type = ASTInterpolatedStringType()
ast_ident_type = ASTIdentType()
ast_int_type = ASTIntType()
ast_float_type = ASTFloatType()
ast_symbol_type = ASTSymbolType()
ast_list_type = ASTListType()
ast_tuple_type = ASTTupleType()
ast_map_type = ASTMapType()
ast_call_type = ASTCallType()
ast_unquote_type = ASTUnquoteType()
ast_binary_slurp_type = ASTBinarySlurpType()
ast_block_type = ASTBlockType()
ast_trailed_type = ASTTrailedType()
