from . import semantics as sem


class Panic(Exception):
    pass
#
#
# def get_attr(obj, *attrs):
#     if isinstance(obj, str):
#         obj = ASTIdent(obj)
#     for attr in attrs:
#         obj = ASTCall(ASTIdent('getattr'), [obj, ASTIdent(attr)])
#     return obj
#
#
# def call(obj, *args):
#     if isinstance(obj, str):
#         obj = ASTIdent(obj)
#     return IdentCall(obj, args)
#
#
# def to_str(obj):
#     return call(get_attr(obj, 'str'))
#


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


class Type(Object):
    def __init__(self, name, parent):
        super().__init__({
            'name': String(name),
            'parent': parent,
            'call': identity,
        }, TypeType)


class PrimMacro(Object):
    def __init__(self, name, args):
        super().__init__({'name': String(name)}, PrimFunType)
        self.name = name
        self.args = args

    def call(self, caller_scope, args):
        args = args.elems
        if not len(args) == len(self.args):
            raise Panic('PrimFun `{}` takes {} arguments, not {}'.format(
                self.name, len(self.args), len(args)))
        return self.macro(caller_scope, *args)


class PrimFun(PrimMacro):
    def macro(self, caller_scope, *args):
        return self.fun(caller_scope, *[caller_scope.eval(arg) for arg in args])


class StringTypeCall(PrimMacro):
    def __init__(self):
        super().__init__('string', ['ast'])

    def macro(self, scope, ast):
        return ast.get('str')


class ReturnException(Exception):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj


class Return(PrimFun):
    def __init__(self):
        super().__init__('return', ['obj'])

    def fun(scope, obj):
        raise ReturnException(obj)


class Fun(Object):
    def __init__(self, defn_scope, args_name, body):
        super().__init__(
            {'body': body, 'args_name': String(args_name), 'defn_scope': defn_scope}, FunType)

    def call(self, caller_scope, args):
        scope = Scope(self.get('defn_scope'))
        args_name = self.get('args_name')
        if not isinstance(args_name, String):
            raise Panic('Args name must be a string')
        scope.set(args_name.str, args)
        scope.set('return', ret)
        body = self.get('body')
        if not isinstance(body, List):
            raise Panic('Function body must be a list')
        try:
            for statement in body.elems[:-1]:
                self.scope.eval(statement)
            return self.scope.eval(body.elems[-1])
        except ReturnException as e:  # hack to use Python's function stack instead of building our own
            return e.obj


class Scope(Object):
    def __init__(self, parent=None):
        super().__init__({}, ScopeType)
        self.get('meta').set('eval', Eval(self))
        self.get('meta').set('scope', self)
        self.get('meta').set('parent', parent if parent is not None else nil)

    def eval(self, ast):
        if isinstance(ast, ASTCall):
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
            string = ast.get('str')
            if not isinstance(string, String):
                raise Exception('Invalid string')
            return StringType.call(self, List([ast]))
        else:
            raise NotImplementedError(
                'Evaluation of node {} not implemented'.format(ast))


class Module(Scope):
    def __init__(self, name, attrs=None, parent=None):
        super().__init__(parent)
        self.get('meta').set('type', ModuleType)
        if attrs is not None:
            self.attrs.update(attrs)
        self.get('meta').set('name', String(name))
        self.get('meta').set('module', self)
        # self.set('self', self)


class String(Object):
    def __init__(self, string):
        super().__init__({}, StringType)
        self.str = string

    def __repr__(self):
        return 'String("{}")'.format(self.str)


class List(Object):
    def __init__(self, elems):
        super().__init__({}, ListType)
        self.elems = elems


class Nil(Object):
    def __init__(self):
        super().__init__({}, NilType)


class ASTIdent(Object):
    def __init__(self, ident):
        super().__init__({'ident': ident}, ASTIdentType)


class ASTCall(Object):
    def __init__(self, callable_expr, args):
        super().__init__(
            {'callable': callable_expr, 'args': args}, ASTCallType)


class ASTString(Object):
    def __init__(self, string):
        super().__init__({'str': string}, ASTStringType)


class ASTList(Object):
    def __init__(self, elems):
        super().__init__({'elems': elems}, ASTListType)


def model_to_ast(model):
    if isinstance(model, sem.Ident):
        return ASTIdent(String(model.identifier))
    elif isinstance(model, sem.Call):
        return ASTCall(model_to_ast(model.callable_expr), List([model_to_ast(arg) for arg in model.args]))
    elif isinstance(model, sem.String):
        return ASTString(String(model.string))
    elif isinstance(model, sem.List):
        return ASTList(List([model_to_ast(elem) for elem in model.elements]))
    else:
        raise NotImplementedError(
            'Translation of model node {} to AST not implemented'.format(model))


class GetAttr(PrimFun):
    def __init__(self):
        super().__init__('get_attr', ['obj', 'attr'])

    def fun(self, scope, obj, attr):
        if not isinstance(attr, String):
            raise Panic('Attribute must be a string')
        return obj.get(attr.str)


class SetAttr(PrimFun):
    def __init__(self):
        super().__init__('set_attr', ['obj', 'attr', 'val'])

    def fun(self, scope, obj, attr, val):
        if not isinstance(attr, String):
            raise Panic('Attribute must be a string')
        return obj.set(attr.str, val)


class Let(PrimFun):
    def __init__(self):
        super().__init__('let', ['name', 'val'])

    def fun(self, scope, name, val):
        if not isinstance(name, String):
            raise Panic('Name must be a string')
        return scope.set(name.str, val)


class Eval(PrimFun):
    def __init__(self, scope):
        super().__init__('eval', ['ast'])
        self.scope = scope

    def fun(self, scope, ast):
        return self.scope.eval(ast)


class Identity(PrimFun):
    def __init__(self):
        super().__init__('identity', ['obj'])

    def fun(self, scope, obj):
        return obj


class Puts(PrimFun):
    def __init__(self):
        super().__init__('puts', ['str'])

    def fun(self, scope, string):
        if not isinstance(string, String):
            raise Panic('Argument must be a string')
        print(string.str)


TypeType = PrimObject({})

meta_obj = PrimObject({})
meta_obj.set('meta', meta_obj)

StringType = Object({}, TypeType)
StringType.set('name', String('String'))
TypeType.set('name', String('Type'))
TypeType.set('meta', PrimObject(
    {'name': String('TypeType'), 'meta': meta_obj}))

ObjectType = Object({'name': String('Object')}, TypeType)
ObjectType.set('parent', ObjectType)
TypeType.set('parent', ObjectType)

PrimFunType = Object(
    {'name': String('PrimFun'), 'parent': ObjectType}, TypeType)
string_type_call = StringTypeCall()
StringType.set('call', string_type_call)

identity = Identity()
TypeType.set('call', identity)
ObjectType.set('call', identity)
PrimFunType.set('call', identity)

MetaType = Type('Meta', TypeType)
meta_obj.set('type', MetaType)

FunType = Type('Fun', ObjectType)
ScopeType = Type('Scope', ObjectType)
ModuleType = Type('Module', ScopeType)

ListType = Type('List', ObjectType)

ret = Return()

NilType = Type('Nil', ObjectType)
nil = Nil()

get_attr = GetAttr()
set_attr = SetAttr()
let = Let()

puts = Puts()

prim = Module('prim', {
    'Type': TypeType,
    'Object': ObjectType,
    'Meta': MetaType,
    'PrimFun': PrimFunType,
    'Fun': FunType,
    'Module': ModuleType,
    'Scope': ScopeType,

    'String': StringType,
    'List': ListType,

    'Nil': NilType,
    'nil': nil,

    'puts': puts,
})

ASTNodeType = Type('Node', ObjectType)
ASTIdentType = Type('Ident', ASTNodeType)
ASTStringType = Type('String', ASTNodeType)
# ASTIntType = Type('Int', ASTNodeType)
# ASTFloatType = Type('Float', ASTNodeType)
# ASTInterpolatedStringType = Type('InterpolatedString', ASTNodeType)
# ASTSymbolType = Type('Symbol', ASTNodeType)
ASTListType = Type('List', ASTNodeType)
# ASTMapType = Type('Map', ASTNodeType)
# ASTTupleType = Type('Tuple', ASTNodeType)
ASTCallType = Type('Call', ASTNodeType)
# ASTPartialCallType = Type('PartialCall', ASTNodeType)
# ASTUnquoteType = Type('Unquote', ASTNodeType)
# ASTBinaryType = Type('Binary', ASTNodeType)
# ASTBinarySlurpType = Type('BinarySlurp', ASTNodeType)
# ASTBlockType = Type('Block', ASTNodeType)

prim.set('ast', Module('ast', {
    'Node': ASTNodeType,
    'Ident': ASTIdentType,
    'String': ASTStringType,
    # 'Int': ASTIntType,
    # 'Float': ASTFloatType,
    # 'InterpolatedString': ASTInterpolatedStringType,
    # 'Symbol': ASTSymbolType,
    'List': ASTListType,
    # 'Tuple': ASTTupleType,
    # 'Map': ASTMapType,
    'Call': ASTCallType,
    # 'PartialCall': ASTPartialCallType,
    # 'Unquote': ASTUnquoteType,
    # 'Binary': ASTBinaryType,
    # 'BinarySlurp': ASTBinarySlurpType,
    # 'Block': ASTBlockType,
}, prim))


builtin_vars = {
    'get_attr': get_attr,
    'set_attr': set_attr,
    'let': let,
}


def load_module(statements, name, preload=None):
    if preload is None:
        preload = {}
    module = Module(name)
    for name, obj in builtin_vars.items():
        module.set(name, obj)
    for name, obj in preload.items():
        module.set(name, obj)
    for statement in statements:
        module.eval(model_to_ast(statement))
