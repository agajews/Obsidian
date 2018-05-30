class Panic(Exception):
    def __init__(self, msg, parseinfo=None, stack=None):
        self.msg = msg
        self.parseinfo = parseinfo
        if stack is None:
            stack = []
        self.stack = stack


def type_name(obj):
    try:
        type = obj.get('meta').get('type')
    except Panic:
        return '[Object has no type]'
    try:
        name = type.get('name')
    except Panic:
        return '[Type has no name]'
    if not isinstance(name, String):
        return '[Type name is not a String]'
    return name.str


def type_type_name(t):
    try:
        name = t.T.get('name')
    except Panic:
        return '[Type has no name]'
    if not isinstance(name, String):
        return '[Type name is not a String]'
    return name.str


class PrimObject:
    def __init__(self, attrs):
        self.attrs = attrs

    def get(self, attr):
        if not attr in self.attrs:
            raise Panic(
                'Object has no attribute `{}`'.format(attr))
        return self.attrs[attr]

    def set(self, name, obj):
        self.attrs[name] = obj

    def has(self, attr):
        return attr in self.attrs

    def typecheck_attr(self, attr, t):
        if not isinstance(self.get(attr), t):
            raise Panic('Attr `{}` of `{}` must be a `{}`, not a `{}`'.format(
                attr, type_name(self), type_type_name(t), type_name(self.get(attr))))

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        # return 'PrimObject({})'.format({k: v for k, v in self.attrs.items() if k != 'meta'})
        type_name = self.get('meta').get('type').get('name')
        if isinstance(type_name, String):
            return '<{}>'.format(type_name.str)
        return '<Object [meta.type.name not a String]>'

    def call(self, caller_scope, args=None):
        if args is None:
            args = []
        if 'call' not in self.attrs:
            raise Panic('Object not callable')
        return self.get('call').call(caller_scope, args)


class Object(PrimObject):
    def __init__(self, attrs):
        super().__init__(attrs)
        self.attrs['meta'] = PrimObject(
            {'type': self.__class__.T, 'meta': meta_obj})


class PrimFun(Object):
    def __init__(self, name, args=None, variadic=False):
        super().__init__({'name': String(name)})
        self.name = name
        assert args is not None or variadic
        self.args = args
        self.variadic = variadic

    def typecheck_arg(self, arg, type):
        if isinstance(type, tuple):
            if not any(isinstance(arg, t) for t in type):
                types_str = ', '.join('`{}`'.format(
                    type_type_name(t)) for t in type)
                raise Panic('Arg `{}` of `{}` must be one of ({}), not a `{}`'.format(
                    arg, self.name, types_str, type_name(arg)))
        else:
            if not isinstance(arg, type):
                raise Panic('Arg `{}` of `{}` must be a `{}`, not a `{}`'.format(
                    arg, self.name, type_type_name(type), type_name(arg)))

    def call(self, caller_scope, args=None):
        if args is None:
            args = []
        if not self.variadic and not len(args) == len(self.args):
            raise Panic('PrimFun `{}` takes {} arguments, not {}'.format(
                self.name, len(self.args), len(args)))
        try:
            res = self.macro(caller_scope, *args)
        except Panic as p:
            raise Panic(p.msg, p.parseinfo, p.stack + [(self, {'args': args})])
        if res is None:
            return nil
        return res

    def macro(self, caller_scope, *args):
        # print('PrimFun {} got args {}'.format(self.name, args))
        return self.fun(*[caller_scope.eval(arg) for arg in args])


class ObjectConstructor(PrimFun):
    def __init__(self):
        super().__init__('Object', ['type'])

    def fun(self, type):
        class NewType(Object):
            T = type
        return NewType({})


class TypeConstructor(PrimFun):
    def __init__(self):
        super().__init__('Object', ['name', 'parent'])

    def fun(self, name, parent):
        self.typecheck_arg(name, String)
        return Type(name.str, parent)


class StringToStr(PrimFun):
    def __init__(self):
        super().__init__('String.to_str', ['str'])

    def fun(self, string):
        self.typecheck_arg(string, String)
        return string


class String(Object):
    def __init__(self, string):
        super().__init__({})
        self.str = string

    def __repr__(self):
        return '"{}"'.format(self.str)


class Type(Object):
    def __init__(self, name, parent, statics=None):
        if statics is None:
            statics = {}
        super().__init__({
            'name': String(name),
            'parent': parent,
            'methods': Object({}),
            'statics': Object(statics),
        })


class NilToStr(PrimFun):
    def __init__(self):
        super().__init__('Nil.to_str', ['str'])

    def fun(self, nil):
        return String('nil')


class Nil(Object):
    def __init__(self):
        super().__init__({})

    def __repr__(self):
        return 'nil'


Type.T = PrimObject({})

meta_obj = PrimObject({})
meta_obj.set('meta', meta_obj)

Object.T = PrimObject({})
Object.T.set('meta', PrimObject({'type': Type.T, 'meta': meta_obj}))
meta_obj.set('type', Object.T)
String.T = PrimObject(
    {'meta': PrimObject({'type': Type.T, 'meta': meta_obj})})
Object.T.set('name', String('Object'))

String.T.set('name', String('String'))
Type.T.set('name', String('Type'))
Type.T.set('meta', PrimObject(
    {'name': String('Type'), 'type': Type.T, 'meta': meta_obj}))

Object.T.set('parent', Object.T)
Object.T.set('methods', Object({}))
Object.T.set('statics', Object({}))
Type.T.set('parent', Object.T)
Type.T.set('methods', Object({}))
Type.T.set('statics', Object({}))
String.T.set('statics', Object({}))
String.T.set('parent', Object.T)

PrimFun.T = PrimObject(
    {'name': String('PrimFun'), 'parent': Object.T, 'meta': PrimObject({'type': Type.T})})
PrimFun.T.set('methods', Object({}))
PrimFun.T.set('statics', Object({}))
Object.T.set('call', ObjectConstructor())
Type.T.set('call', TypeConstructor())
String.T.set('methods', Object({'to_str': StringToStr()}))

Nil.T = Type('Nil', Object.T)
nil = Nil()
