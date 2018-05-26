from .. import semantics as sem
from .bootstrap import (
    Panic, PrimObject, Object, String, PrimFun, Type,
    type_type, string_type, object_type, prim_fun_type, meta_type, nil_type,
    nil
)


class FunType(Type):
    def __init__(self):
        super().__init__('Fun', object_type, ['body'])

    def macro(self, scope, body):
        return Fun(scope, scope.eval(body))


class ScopeType(Type):
    def __init__(self):
        super().__init__('Scope', object_type, ['parent'])

    def fun(self, parent):
        if parent is nil:
            return Scope()
        return Scope(parent)


class ModuleType(Type):
    def __init__(self):
        super().__init__('Module', scope_type, ['name', 'parent'])

    def fun(self, name, parent):
        if parent is nil:
            return Module(name)
        return Module(name, parent)


class ASTNodeType(Type):
    def __init__(self):
        super().__init__('Node', object_type, [])


class ASTIdentType(Type):
    def __init__(self):
        super().__init__('Ident', ast_node_type, ['ident'])

    def fun(self, ident):
        return ASTIdent(ident)


class ASTStringType(Type):
    def __init__(self):
        super().__init__('String', ast_node_type, ['str'])

    def fun(self, string):
        return ASTString(string)


class ASTIntType(Type):
    def __init__(self):
        super().__init__('Int', ast_node_type, ['int'])

    def fun(self, val):
        return ASTInt(val)


class ASTListType(Type):
    def __init__(self):
        super().__init__('List', ast_node_type, ['list'])

    def fun(self, lst):
        return ASTList(lst)


class ASTBinarySlurpType(Type):
    def __init__(self):
        super().__init__('BinarySlurp', ast_node_type, ['slurp'])

    def fun(self, slurp):
        return ASTBinarySlurp(slurp)


class ASTCallType(Type):
    def __init__(self):
        super().__init__('Call', ast_node_type, ['callable', 'args'])

    def fun(self, callable_expr, args):
        return ASTCall(callable_expr, args)


class ListType(Type):
    def __init__(self):
        super().__init__('List', object_type, ['ast'])

    def macro(self, scope, ast):
        elems = ast.get('elems')
        if not isinstance(elems, List):
            raise Panic('Invalid list')
        return List([scope.eval(elem) for elem in elems.elems])


class IntType(Type):
    def __init__(self):
        super().__init__('Int', object_type, ['ast'],
                         methods={'to_str': IntToStr()})

    def macro(self, scope, ast):
        int = ast.get('int')
        if not isinstance(int, Int):
            raise Panic('Invalid int')
        return Int(int.int)


class IntToStr(PrimFun):
    def __init__(self):
        super().__init__('to_str', ['int'])

    def fun(self, int):
        return String(str(int.int))


class ReturnException(Exception):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj


class Return(PrimFun):
    def __init__(self):
        super().__init__('return', ['obj'])

    def fun(obj):
        raise ReturnException(obj)


class Fun(Object):
    def __init__(self, defn_scope, body):
        super().__init__(
            {'body': body, 'defn_scope': defn_scope}, fun_type)
        # print(f'Created fun with body {body}')

    def call(self, caller_scope, args):
        scope = Scope(self.get('defn_scope'))
        scope.get('meta').set('args', List(args))
        scope.set('return', ret)
        body = self.get('body')
        if not isinstance(body, List):
            raise Panic('Function body must be a list')
        try:
            for statement in body.elems[:-1]:
                scope.eval(statement)
            return scope.eval(body.elems[-1])
        except ReturnException as e:  # hack to use Python's function stack instead of building our own
            return e.obj

    def __repr__(self):
        return 'Fun({})'.format(self.body)


class Scope(Object):
    def __init__(self, parent=None):
        super().__init__({}, scope_type)
        self.get('meta').set('eval', Eval(self))
        self.get('meta').set('scope', self)
        self.get('meta').set('parent', parent if parent is not None else nil)

    def eval(self, ast):
        if isinstance(ast, ASTCall):
            # print(f'Calling {ast}')
            return self.eval(ast.get('callable')).call(self, ast.get('args').elems)
        elif isinstance(ast, ASTIdent):
            ident = ast.get('ident')
            if not isinstance(ident, String):
                raise Panic('Invalid ident')
            ident = ident.str
            if ident in self.attrs:
                return self.get(ident)
            if self.get('meta').get('parent') is not nil:
                return self.get('meta').get('parent').eval(ast)
            raise Panic('No such object `{}`'.format(ident))
        elif isinstance(ast, ASTString):
            return string_type.call(self, [ast])
        elif isinstance(ast, ASTInt):
            return int_type.call(self, [ast])
        elif isinstance(ast, ASTList):
            return list_type.call(self, [ast])
        elif isinstance(ast, ASTBinarySlurp):
            raise Panic('Got binary slurp {}'.format(ast))
        else:
            raise NotImplementedError(
                'Evaluation of node {} not implemented'.format(ast))


class Module(Scope):
    def __init__(self, name, parent=None, attrs=None):
        super().__init__(parent=parent)
        self.get('meta').set('type', module_type)
        if attrs is not None:
            self.attrs.update(attrs)
        self.get('meta').set('name', String(name))
        self.get('meta').set('module', self)
        # self.set('self', self)


class Int(Object):
    def __init__(self, val):
        super().__init__({}, int_type)
        self.int = val

    def __repr__(self):
        return str(self.int)


class List(Object):
    def __init__(self, elems):
        super().__init__({}, list_type)
        self.elems = elems

    def __repr__(self):
        return str(self.elems)


class ASTIdent(Object):
    def __init__(self, ident):
        if not isinstance(ident, String):
            raise Panic('Invalid ident')
        super().__init__({'ident': ident}, ast_ident_type)

    def __repr__(self):
        return 'ASTIdent({})'.format(self.get("ident"))


class ASTCall(Object):
    def __init__(self, callable_expr, args):
        super().__init__(
            {'callable': callable_expr, 'args': args}, ast_call_type)

    def __repr__(self):
        return 'ASTCall({}, {})'.format(self.get("callable"), self.get("args"))


class ASTString(Object):
    def __init__(self, string, sigil=None):
        if not isinstance(string, String):
            raise Panic('Invalid string')
        if sigil is not None and not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        super().__init__(
            {'str': string, 'sigil': nil if sigil is None else sigil}, ast_string_type)

    def __repr__(self):
        return 'ASTString({}, {})'.format(self.get("str"), self.get("sigil"))


class ASTInt(Object):
    def __init__(self, val, sigil=None):
        if not isinstance(val, Int):
            raise Panic('Invalid int')
        if sigil is not None and not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        super().__init__(
            {'int': val, 'sigil': nil if sigil is None else sigil}, ast_int_type)

    def __repr__(self):
        return 'ASTInt({}, {})'.format(self.get("int"), self.get("sigil"))


class ASTList(Object):
    def __init__(self, elems):
        if not isinstance(elems, List):
            raise Panic('Invalid list')
        super().__init__({'elems': elems}, ast_list_type)

    def __repr__(self):
        return 'ASTList({})'.format(self.get("elems"))


class ASTBinarySlurp(Object):
    def __init__(self, slurp):
        if not isinstance(slurp, List):
            raise Panic('Invalid slurp')
        super().__init__({'slurp': slurp}, ast_binary_slurp_type)


def model_to_ast(model):
    if isinstance(model, sem.Ident):
        return ASTIdent(String(model.identifier))
    elif isinstance(model, sem.Call):
        return ASTCall(model_to_ast(model.callable_expr), List([model_to_ast(arg) for arg in model.args]))
    elif isinstance(model, sem.String):
        return ASTString(String(model.string), String(model.sigil) if model.sigil is not None else None)
    elif isinstance(model, sem.Int):
        return ASTInt(Int(model.val), String(model.sigil) if model.sigil is not None else None)
    elif isinstance(model, sem.List):
        return ASTList(List([model_to_ast(elem) for elem in model.elements]))
    elif isinstance(model, sem.BinarySlurp):
        return ASTBinarySlurp(List([model_to_ast(elem) for elem in model.slurp]))
    else:
        raise NotImplementedError(
            'Translation of model node {} to AST not implemented'.format(model))


class MethodFun(PrimFun):
    def __init__(self, obj, method):
        super().__init__('method_fun', variadic=True)
        self.obj = obj
        self.method = method

    def macro(self, scope, *args):
        obj_scope = Scope(scope)
        obj_scope.set('__self__', self.obj)
        return self.method.call(obj_scope, [ASTIdent(String('__self__'))] + list(args))


class GetAttr(PrimFun):
    def __init__(self):
        super().__init__('get_attr', ['obj', 'attr'])

    def fun(self, obj, attr):
        if not isinstance(attr, String):
            raise Panic('Attribute must be a string')
        if not obj.has(attr.str):
            obj_type = obj.get('meta').get('type')
            if obj_type.get('methods').has(attr.str):
                return MethodFun(obj, obj_type.get('methods').get(attr.str))
            if obj_type.get('statics').has(attr.str):
                return obj_type.get('statics').get(attr.str)
        return obj.get(attr.str)


class SetAttr(PrimFun):
    def __init__(self):
        super().__init__('set_attr', ['obj', 'attr', 'val'])

    def fun(self, obj, attr, val):
        if not isinstance(attr, String):
            raise Panic('Attribute must be a string')
        return obj.set(attr.str, val)


class Let(PrimFun):
    def __init__(self):
        super().__init__('let', ['name', 'val'])

    def macro(self, scope, name, val):
        name = scope.eval(name)
        val = scope.eval(val)
        if not isinstance(name, String):
            raise Panic('Name must be a string')
        return scope.set(name.str, val)


class Eval(PrimFun):
    def __init__(self, scope):
        super().__init__('eval', ['ast'])
        self.scope = scope

    def fun(self, ast):
        return self.scope.eval(ast)


# class Identity(PrimFun):
#     def __init__(self):
#         super().__init__('identity', ['obj'])
#
#     def fun(self, obj):
#         return obj
#

class Puts(PrimFun):
    def __init__(self):
        super().__init__('puts', ['str'])

    def fun(self, string):
        if not isinstance(string, String):
            raise Panic('Argument must be a string')
        print(string.str)


fun_type = FunType()
scope_type = ScopeType()
module_type = ModuleType()

list_type = ListType()
int_type = IntType()

ret = Return()

get_attr = GetAttr()
set_attr = SetAttr()
let = Let()

puts = Puts()

prim = Module('prim', attrs={
    'Type': type_type,
    'Object': object_type,
    'Meta': meta_type,
    'PrimFun': prim_fun_type,
    'Fun': fun_type,
    'Module': module_type,
    'Scope': scope_type,

    'String': string_type,
    'List': list_type,
    'Int': int_type,

    'Nil': nil_type,
    'nil': nil,

    'let': let,

    'puts': puts,
})

ast_node_type = ASTNodeType()
ast_ident_type = ASTIdentType()
ast_string_type = ASTStringType()
ast_int_type = ASTIntType()
# ASTFloatType = Type('Float', ASTNodeType)
# ASTInterpolatedStringType = Type('InterpolatedString', ASTNodeType)
# ASTSymbolType = Type('Symbol', ASTNodeType)
ast_list_type = ASTListType()
# ASTMapType = Type('Map', ASTNodeType)
# ASTTupleType = Type('Tuple', ASTNodeType)
ast_call_type = ASTCallType()
# ASTPartialCallType = Type('PartialCall', ASTNodeType)
# ASTUnquoteType = Type('Unquote', ASTNodeType)
ast_binary_slurp_type = ASTBinarySlurpType()
# ASTBlockType = Type('Block', ASTNodeType)

prim.set('ast', Module('ast', parent=prim, attrs={
    'Node': ast_node_type,
    'Ident': ast_ident_type,
    'String': ast_string_type,
    'Int': ast_int_type,
    # 'Float': ASTFloatType,
    # 'InterpolatedString': ASTInterpolatedStringType,
    # 'Symbol': ASTSymbolType,
    'List': ast_list_type,
    # 'Tuple': ASTTupleType,
    # 'Map': ASTMapType,
    'Call': ast_call_type,

    # 'Unquote': ASTUnquoteType,
    # 'Binary': ASTBinaryType,
    'BinarySlurp': ast_binary_slurp_type,
    # 'Block': ASTBlockType,
}))


builtin_vars = {
    'get_attr': get_attr,
    'set_attr': set_attr,
}


def load_module(statements, source_map, name, preload=None):
    if preload is None:
        preload = {}
    module = Module(name)
    for name, obj in builtin_vars.items():
        module.set(name, obj)
    for name, obj in preload.items():
        module.set(name, obj)
    for statement in statements:
        module.eval(model_to_ast(statement))
