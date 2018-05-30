from ..types import (
    PrimFun,
    Panic,
    String,
    Int,
    Float,
    Symbol,
    List,
    Tuple,
)
from ..types.scope import to_str
from ..types.ast import (
    ASTString,
    ASTInterpolatedString,
    ASTIdent,
    ASTInt,
    ASTFloat,
    ASTSymbol,
    ASTList,
    ASTTuple,
    ASTMap,
    ASTBlock,
    ASTCall,
)


def ast_to_str(scope, ast, first=True):
    if isinstance(ast, ASTCall):
        if len(ast.args_list()) > 0:
            return '({} {})'.format(
                ast_to_str(scope, ast.get('callable'), first=False),
                ' '.join(ast_to_str(scope, arg, first=False) for arg in ast.args_list()))
        else:
            return '({})'.format(ast_to_str(scope, ast.get('callable'), first=False))
    elif isinstance(ast, ASTIdent):
        if first:
            return '{{{}}}'.format(to_str(scope, ast.get('ident')))
        else:
            return '{}'.format(to_str(scope, ast.get('ident')))
    elif isinstance(ast, ASTString):
        if first:
            return "{{{}'{}'}}".format(
                to_str(scope, ast.get('sigil')),
                to_str(scope, ast.get('str')))
        else:
            return "{}'{}'".format(
                to_str(scope, ast.get('sigil')),
                to_str(scope, ast.get('str')))
    elif isinstance(ast, ASTInterpolatedString):
        return '"{}"'.format(''.join(
            ast_to_str(scope, body, first=False) for body in ast.body_list()))
    elif isinstance(ast, ASTInt):
        if first:
            return '{{{}}}'.format(to_str(scope, ast.get('int')))
        else:
            return '{}'.format(to_str(scope, ast.get('int')))
    elif isinstance(ast, ASTFloat):
        if first:
            return '{{{}}}'.format(to_str(scope, ast.get('float')))
        else:
            return '{}'.format(to_str(scope, ast.get('float')))
    elif isinstance(ast, ASTSymbol):
        if first:
            return '{{{}}}'.format(to_str(scope, ast.get('symbol')))
        else:
            return '{}'.format(to_str(scope, ast.get('symbol')))
    elif isinstance(ast, ASTList):
        if first:
            return '{{[{}]}}'.format(', '.join(
                ast_to_str(scope, body, first=False) for body in ast.elems_list()))
        else:
            return '[{}]'.format(', '.join(
                ast_to_str(scope, body, first=False) for body in ast.elems_list()))
    elif isinstance(ast, ASTBlock):
        if first:
            return '{{{}}}'.format('; '.join(
                ast_to_str(scope, body, first=False) for body in ast.statements_list()))
        else:
            return '{}'.format('; '.join(
                ast_to_str(scope, body, first=False) for body in ast.statements_list()))
    elif isinstance(ast, ASTTuple):
        if first:
            return '{{({})}}'.format(', '.join(
                ast_to_str(scope, body, first=False) for body in ast.elems_list()))
        else:
            return '({})'.format(', '.join(
                ast_to_str(scope, body, first=False) for body in ast.elems_list()))
    elif isinstance(ast, ASTMap):
        if first:
            return '{{ {{{}}} }}'.format(', '.join(
                ast_to_str(scope, body, first=False) for body in ast.elems_list()))
        else:
            return '{{{}}}'.format(', '.join(
                ast_to_str(scope, body, first=False) for body in ast.elems_list()))
    else:
        return '<ast {}>'.format(type(ast))


class ASTStringConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.String', ['str', 'sigil'])

    def fun(self, string, sigil):
        self.typecheck_arg(string, String)
        self.typecheck_arg(sigil, String)
        return ASTString(string, sigil)


class ASTStringToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.String.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        self.typecheck_arg(ast, ASTString)
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTIdentConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Ident', ['ident'])

    def fun(self, ident):
        self.typecheck_arg(ident, String)
        return ASTIdent(ident)


class ASTIdentToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Ident.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        self.typecheck_arg(ast, ASTIdent)
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTCallConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Call', ['callable', 'args'])

    def fun(self, callable_expr, args):
        self.typecheck_arg(args, List)
        return ASTCall(callable_expr, args)


class ASTCallToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Call.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        self.typecheck_arg(ast, ASTCall)
        # TODO: treat infix ops differently
        # fn_name = ast.get('callable').get('name')
        # if isinstance(fn_name, String) and fn_name == '{.}' and len(ast.args_list()) == 2:
        #     return String('{{{}.{}}}'.format())
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTInterpolatedStringConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.InterpolatedString', ['body'])

    def fun(self, body):
        self.typecheck_arg(body, List)
        return ASTInterpolatedString(body)


class ASTInterpolatedStringToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.InterpolatedString.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTInterpolatedString):
            raise Panic('Argument must be an ast.InterpolatedString')
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTIntConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Int', ['int', 'sigil'])

    def fun(self, val, sigil):
        self.typecheck_arg(val, Int)
        self.typecheck_arg(sigil, String)
        return ASTInt(val, sigil)


class ASTIntToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Int.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        self.typecheck_arg(ast, ASTInt)
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTFloatConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Float', ['float', 'sigil'])

    def fun(self, val, sigil):
        self.typecheck_arg(val, Float)
        self.typecheck_arg(sigil, String)
        return ASTFloat(val, sigil)


class ASTFloatToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Float.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        self.typecheck_arg(ast, ASTFloat)
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTSymbolConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Symbol', ['symbol'])

    def fun(self, symbol):
        self.typecheck_arg(symbol, Symbol)
        return ASTSymbol(symbol)


class ASTSymbolToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Symbol.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        self.typecheck_arg(ast, ASTSymbol)
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTListConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.List', ['list'])

    def fun(self, lst):
        self.typecheck_arg(lst)
        return ASTList(lst, List)


class ASTListToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.List.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        self.typecheck_arg(ast, ASTList)
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTTupleConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Tuple', ['tuple'])

    def fun(self, tup):
        self.typecheck_arg(tup, Tuple)
        return ASTTuple(tup)


class ASTTupleToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Tuple.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        self.typecheck_arg(ast, ASTTuple)
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTMapConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Map', ['map'])

    def fun(self, lst):
        self.typecheck_arg(lst, List)
        return ASTMap(lst)


class ASTMapToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Map.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        self.typecheck_arg(ast, ASTMap)
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTBlockConstructor(PrimFun):
    def __init__(self):
        super().__init__('ast.Block', ['statements'])

    def fun(self, statements):
        self.typecheck_arg(statements, List)
        return ASTBlock(statements)


class ASTBlockToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Block.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        self.typecheck_arg(ast, ASTBlock)
        return String(ast_to_str(scope, scope.preprocess(ast)))

#
# class ASTBinarySlurpConstructor(PrimFun):
#     def __init__(self):
#         super().__init__('ast.BinarySlurp', ['slurp'])
#
#     def fun(self, slurp):
#         self.typecheck_arg(slurp, List)
#         return ASTBinarySlurp(slurp)
#
#
# class ASTUnquoteConstructor(PrimFun):
#     def __init__(self):
#         super().__init__('ast.Unquote', ['expr'])
#
#     def fun(self, expr):
#         return ASTUnquote(expr)
#


ASTString.T.set('call', ASTStringConstructor())
ASTString.T.get('methods').set('to_str', ASTStringToStr())

ASTInterpolatedString.T.set('call', ASTInterpolatedStringConstructor())
ASTInterpolatedString.T.get('methods').set(
    'to_str', ASTInterpolatedStringToStr())

ASTIdent.T.set('call', ASTIdentConstructor())
ASTIdent.T.get('methods').set('to_str', ASTIdentToStr())

ASTInt.T.set('call', ASTIntConstructor())
ASTInt.T.get('methods').set('to_str', ASTIntToStr())

ASTFloat.T.set('call', ASTFloatConstructor())
ASTFloat.T.get('methods').set('to_str', ASTFloatToStr())

ASTSymbol.T.set('call', ASTSymbolConstructor())
ASTSymbol.T.get('methods').set('to_str', ASTSymbolToStr())

ASTList.T.set('call', ASTListConstructor())
ASTList.T.get('methods').set('to_str', ASTListToStr())

ASTTuple.T.set('call', ASTTupleConstructor())
ASTTuple.T.get('methods').set('to_str', ASTTupleToStr())

ASTMap.T.set('call', ASTMapConstructor())
ASTMap.T.get('methods').set('to_str', ASTMapToStr())

ASTBlock.T.set('call', ASTBlockConstructor())
ASTBlock.T.get('methods').set('to_str', ASTBlockToStr())

ASTCall.T.set('call', ASTCallConstructor())
ASTCall.T.get('methods').set('to_str', ASTCallToStr())


# ast_binary_slurp_type.set('call', ASTBinarySlurpConstructor())
#
# ast_unquote_type.set('call', ASTUnquoteConstructor())
