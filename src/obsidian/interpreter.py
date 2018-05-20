from . import semantics as sem


class Panic(Exception):
    pass


class PrimObject:
    def __init__(self, attrs):
        self.attrs = attrs

    def get(self, attr):
        if not attr in self.attrs:
            raise Panic(
                'Object has no attribute {}'.format(attr))
        return self.attrs[attr]

    def set(self, name, obj):
        self.attrs[name] = obj


class Object(PrimObject):
    def __init__(self, attrs, type):
        super().__init__(attrs)
        self.attrs['meta'] = PrimObject({'type': type, 'meta': meta_obj})

    def call(self, caller_scope, args):
        if 'call' not in self.attrs:
            raise Panic('Object not callable')
        return self.get('call').call(caller_scope, args)


class PrimFun(Object):
    def __init__(self, name, args, type=None):
        super().__init__({'name': String(name)},
                         prim_fun_type if type is None else type)
        self.name = name
        self.args = args

    def call(self, caller_scope, args):
        args = args.elems
        if not len(args) == len(self.args):
            raise Panic('PrimFun `{}` takes {} arguments, not {}'.format(
                self.name, len(self.args), len(args)))
        return self.macro(caller_scope, *args)

    def macro(self, caller_scope, *args):
        return self.fun(*[caller_scope.eval(arg) for arg in args])


class Type(PrimFun):
    def __init__(self, name, parent, args):
        super().__init__(name, args, type_type)
        self.set('parent', parent)

    def fun(self, *args):
        return nil


class FunType(Type):

    def __init__(self):
        super().__init__('Fun', object_type, ['body'])

    def macro(self, scope, body):
        return Fun(scope, scope.eval(body))


class MetaType(Type):
    def __init__(self):
        super().__init__('Meta', object_type, [])

    def fun(self):
        return Meta()


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


class NilType(Type):
    def __init__(self):
        super().__init__('Nil', object_type, [])

    def fun(self):
        return nil


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


class ASTListType(Type):
    def __init__(self):
        super().__init__('List', ast_node_type, ['list'])

    def fun(self, lst):
        return ASTList(lst)


class ASTCallType(Type):
    def __init__(self):
        super().__init__('Call', ast_node_type, ['callable', 'args'])

    def fun(self, callable_expr, args):
        return ASTCall(callable_expr, args)


class StringTypeCall(PrimFun):
    def __init__(self):
        super().__init__('String', ['ast'])

    def macro(self, scope, ast):
        string = ast.get('str')
        if not isinstance(string, String):
            raise Panic('Invalid string')
        sigil = ast.get('sigil')
        if sigil is not nil and not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        if sigil is nil:
            return string
        raise Panic(f'Sigil {sigil.str} not implemented')


class ListType(Type):
    def __init__(self):
        super().__init__('List', object_type, ['ast'])

    def macro(self, scope, ast):
        elems = ast.get('elems')
        if not isinstance(elems, List):
            raise Panic('Invalid list')
        return List([scope.eval(elem) for elem in elems.elems])


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
        scope.get('meta').set('args', args)
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
        return f'Fun({self.body})'


class Meta(Object):
    def __init__(self, **attrs):
        attrs['meta'] = meta_obj
        super().__init__(attrs, meta_type)


class Scope(Object):
    def __init__(self, parent=None):
        super().__init__({}, scope_type)
        self.get('meta').set('eval', Eval(self))
        self.get('meta').set('scope', self)
        self.get('meta').set('parent', parent if parent is not None else nil)

    def eval(self, ast):
        if isinstance(ast, ASTCall):
            # print(f'Calling {ast}')
            return self.eval(ast.get('callable')).call(self, ast.get('args'))
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
            return string_type.call(self, List([ast]))
        elif isinstance(ast, ASTList):
            return list_type.call(self, List([ast]))
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


class String(Object):
    def __init__(self, string):
        super().__init__({}, string_type)
        self.str = string

    def __repr__(self):
        return '"{}"'.format(self.str)


class List(Object):
    def __init__(self, elems):
        super().__init__({}, list_type)
        self.elems = elems

    def __repr__(self):
        return f'{self.elems}'


class Nil(Object):
    def __init__(self):
        super().__init__({}, nil_type)

    def __repr__(self):
        return 'nil'


class ASTIdent(Object):
    def __init__(self, ident):
        if not isinstance(ident, String):
            raise Panic('Invalid ident')
        super().__init__({'ident': ident}, ast_ident_type)

    def __repr__(self):
        return f'ASTIdent({self.get("ident")})'


class ASTCall(Object):
    def __init__(self, callable_expr, args):
        super().__init__(
            {'callable': callable_expr, 'args': args}, ast_call_type)

    def __repr__(self):
        return f'ASTCall({self.get("callable")}, {self.get("args")})'


class ASTString(Object):
    def __init__(self, string, sigil=None):
        if not isinstance(string, String):
            raise Panic('Invalid string')
        if sigil is not None and not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        super().__init__(
            {'str': string, 'sigil': nil if sigil is None else sigil}, ast_string_type)

    def __repr__(self):
        return f'ASTString({self.get("str")}, {self.get("sigil")})'


class ASTList(Object):
    def __init__(self, elems):
        if not isinstance(elems, List):
            raise Panic('Invalid list')
        super().__init__({'elems': elems}, ast_list_type)

    def __repr__(self):
        return f'ASTList({self.get("elems")})'


def model_to_ast(model):
    if isinstance(model, sem.Ident):
        return ASTIdent(String(model.identifier))
    elif isinstance(model, sem.Call):
        return ASTCall(model_to_ast(model.callable_expr), List([model_to_ast(arg) for arg in model.args]))
    elif isinstance(model, sem.String):
        return ASTString(String(model.string), String(model.sigil) if model.sigil is not None else None)
    elif isinstance(model, sem.List):
        return ASTList(List([model_to_ast(elem) for elem in model.elements]))
    else:
        raise NotImplementedError(
            'Translation of model node {} to AST not implemented'.format(model))


class GetAttr(PrimFun):
    def __init__(self):
        super().__init__('get_attr', ['obj', 'attr'])

    def fun(self, obj, attr):
        if not isinstance(attr, String):
            raise Panic('Attribute must be a string')
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

    def fun(self):
        return self.scope.eval(ast)


class Identity(PrimFun):
    def __init__(self):
        super().__init__('identity', ['obj'])

    def fun(self, obj):
        return obj


class Puts(PrimFun):
    def __init__(self):
        super().__init__('puts', ['str'])

    def fun(self, string):
        if not isinstance(string, String):
            raise Panic('Argument must be a string')
        print(string.str)


type_type = PrimObject({})

meta_obj = PrimObject({})
meta_obj.set('meta', meta_obj)

string_type = Object({}, type_type)
string_type.set('name', String('String'))
type_type.set('name', String('Type'))
type_type.set('meta', PrimObject(
    {'name': String('Type'), 'type': type_type, 'meta': meta_obj}))

object_type = Object({'name': String('Object')}, type_type)
object_type.set('parent', object_type)
type_type.set('parent', object_type)

prim_fun_type = Object(
    {'name': String('PrimFun'), 'parent': object_type}, type_type)
string_type_call = StringTypeCall()
string_type.set('call', string_type_call)

identity = Identity()
# type_type.set('call', identity)
# object_type.set('call', identity)
# prim_fun_type.set('call', identity)

meta_type = MetaType()
# meta_type = Type('Meta', type_type)
meta_obj.set('type', meta_type)

fun_type = FunType()
scope_type = ScopeType()
# ScopeType = Type('Scope', object_type)
module_type = ModuleType()
# module_type = Type('Module', scope_type)

list_type = ListType()
# list_type = Type('List', object_type)

ret = Return()

nil_type = NilType()
nil = Nil()

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

    'Nil': NilType,
    'nil': nil,

    'let': let,

    'puts': puts,
})

ast_node_type = ASTNodeType()
ast_ident_type = ASTIdentType()
ast_string_type = ASTStringType()
# ASTIntType = Type('Int', ASTNodeType)
# ASTFloatType = Type('Float', ASTNodeType)
# ASTInterpolatedStringType = Type('InterpolatedString', ASTNodeType)
# ASTSymbolType = Type('Symbol', ASTNodeType)
ast_list_type = ASTListType()
# ASTMapType = Type('Map', ASTNodeType)
# ASTTupleType = Type('Tuple', ASTNodeType)
ast_call_type = ASTCallType()
# ASTPartialCallType = Type('PartialCall', ASTNodeType)
# ASTUnquoteType = Type('Unquote', ASTNodeType)
# ASTBinaryType = Type('Binary', ASTNodeType)
# ASTBinarySlurpType = Type('BinarySlurp', ASTNodeType)
# ASTBlockType = Type('Block', ASTNodeType)

prim.set('ast', Module('ast', parent=prim, attrs={
    'Node': ast_node_type,
    'Ident': ast_ident_type,
    'String': ast_string_type,
    # 'Int': ASTIntType,
    # 'Float': ASTFloatType,
    # 'InterpolatedString': ASTInterpolatedStringType,
    # 'Symbol': ASTSymbolType,
    'List': ast_list_type,
    # 'Tuple': ASTTupleType,
    # 'Map': ASTMapType,
    'Call': ast_call_type,


    # 'PartialCall': ASTPartialCallType,
    # 'Unquote': ASTUnquoteType,
    # 'Binary': ASTBinaryType,
    # 'BinarySlurp': ASTBinarySlurpType,
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
