from ..types import (
    PrimFun,
    Panic,
    String,
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
    ast_string_type,
    ast_interpolated_string_type,
    ast_ident_type,
    ast_int_type,
    ast_float_type,
    ast_symbol_type,
    ast_list_type,
    ast_tuple_type,
    ast_map_type,
    ast_block_type,
    ast_call_type,
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


class ASTStringToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.String.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTString):
            raise Panic('Argument must be an ast.String')
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTIdentToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Ident.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTIdent):
            raise Panic('Argument must be an ast.Ident')
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTCallToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Call.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTCall):
            raise Panic('Argument must be an ast.Call')
        # TODO: treat infix ops differently
        # fn_name = ast.get('callable').get('name')
        # if isinstance(fn_name, String) and fn_name == '{.}' and len(ast.args_list()) == 2:
        #     return String('{{{}.{}}}'.format())
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTInterpolatedStringToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.InterpolatedString.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTInterpolatedString):
            raise Panic('Argument must be an ast.InterpolatedString')
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTIntToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Int.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTInt):
            raise Panic('Argument must be an ast.Int')
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTFloatToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Float.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTFloat):
            raise Panic('Argument must be an ast.Float')
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTSymbolToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Symbol.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTSymbol):
            raise Panic('Argument must be an ast.Symbol')
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTListToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.List.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTList):
            raise Panic('Argument must be an ast.List')
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTTupleToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Tuple.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTTuple):
            raise Panic('Argument must be an ast.Tuple')
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTMapToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Map.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTMap):
            raise Panic('Argument must be an ast.Map')
        return String(ast_to_str(scope, scope.preprocess(ast)))


class ASTBlockToStr(PrimFun):
    def __init__(self):
        super().__init__('ast.Block.to_str', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        if not isinstance(ast, ASTBlock):
            raise Panic(
                'Argument must be an ast.Block, not a `{}`'.format(type(ast)))
        return String(ast_to_str(scope, scope.preprocess(ast)))


ast_string_type.get('methods').set('to_str', ASTStringToStr())
ast_interpolated_string_type.get('methods').set(
    'to_str', ASTInterpolatedStringToStr())
ast_ident_type.get('methods').set('to_str', ASTIdentToStr())
ast_int_type.get('methods').set('to_str', ASTIntToStr())
ast_float_type.get('methods').set('to_str', ASTFloatToStr())
ast_symbol_type.get('methods').set('to_str', ASTSymbolToStr())
ast_list_type.get('methods').set('to_str', ASTListToStr())
ast_tuple_type.get('methods').set('to_str', ASTTupleToStr())
ast_map_type.get('methods').set('to_str', ASTMapToStr())
ast_block_type.get('methods').set('to_str', ASTBlockToStr())
ast_call_type.get('methods').set('to_str', ASTCallToStr())
