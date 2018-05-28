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

    def has(self, attr):
        return attr in self.attrs

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return 'PrimObject({})'.format({k: v for k, v in self.attrs.items() if k != 'meta'})

    def call(self, caller_scope, args=None):
        if args is None:
            args = []
        if 'call' not in self.attrs:
            raise Panic('Object not callable')
        return self.get('call').call(caller_scope, args)


class Object(PrimObject):
    def __init__(self, attrs, type=None):
        super().__init__(attrs)
        if type is None:
            type = object_type
        self.attrs['meta'] = PrimObject({'type': type, 'meta': meta_obj})


class PrimFun(Object):
    def __init__(self, name, args=None, type=None, variadic=False):
        super().__init__({'name': String(name)},
                         prim_fun_type if type is None else type)
        self.name = name
        assert args is not None or variadic
        self.args = args
        self.variadic = variadic

    def call(self, caller_scope, args=None):
        if args is None:
            args = []
        if not self.variadic and not len(args) == len(self.args):
            raise Panic('PrimFun `{}` takes {} arguments, not {}'.format(
                self.name, len(self.args), len(args)))
        return self.macro(caller_scope, *args)

    def macro(self, caller_scope, *args):
        # print('PrimFun {} got args {}'.format(self.name, args))
        return self.fun(*[caller_scope.eval(arg) for arg in args])


class ObjectConstructor(PrimFun):
    def __init__(self):
        super().__init__('Object', ['type'])

    def fun(self, type):
        return Object({}, type)


class TypeConstructor(PrimFun):
    def __init__(self):
        super().__init__('Object', ['name', 'parent'])

    def fun(self, name, parent):
        if not isinstance(name, String):
            raise Panic('Name must be a string')
        return Type(name.str, parent)


class StringConstructor(PrimFun):
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
        raise Panic('Sigil {} not implemented'.format(sigil.str))


class StringToStr(PrimFun):
    def __init__(self):
        super().__init__('to_str', ['str'])

    def fun(self, string):
        if not isinstance(string, String):
            raise Panic('Argument must be a string')
        return string


class String(Object):
    def __init__(self, string):
        super().__init__({}, string_type)
        self.str = string

    def __repr__(self):
        return '"{}"'.format(self.str)


class Type(Object):
    def __init__(self, name, parent, methods=None, statics=None, constructor=None):
        if methods is None:
            methods = {}
        if statics is None:
            statics = {}
        super().__init__({
            'name': String(name),
            'parent': parent,
            'methods': Object(methods),
            'statics': Object(statics),
        }, type_type)
        if constructor is not None:
            self.set('call', constructor)


class MetaType(Type):
    def __init__(self):
        super().__init__('Meta', object_type)


class NilType(Type):
    def __init__(self):
        super().__init__('Nil', object_type)


class Nil(Object):
    def __init__(self):
        super().__init__({}, nil_type)

    def __repr__(self):
        return 'nil'


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
object_type.set('methods', Object({}, object_type))
object_type.set('statics', Object({}, object_type))
type_type.set('parent', object_type)
type_type.set('methods', Object({}, object_type))
type_type.set('statics', Object({}, object_type))
string_type.set('statics', Object({}, object_type))
string_type.set('parent', object_type)

prim_fun_type = Object(
    {'name': String('PrimFun'), 'parent': object_type}, type_type)
prim_fun_type.set('methods', Object({}, object_type))
prim_fun_type.set('statics', Object({}, object_type))
string_type.set('call', StringConstructor())
object_type.set('call', ObjectConstructor())
type_type.set('call', TypeConstructor())
string_type.set('methods', Object({'to_str': StringToStr()}, object_type))

meta_type = MetaType()
meta_type.set('methods', Object({}, object_type))
meta_type.set('statics', Object({}, object_type))
meta_type.set('parent', object_type)
meta_obj.set('type', meta_type)

nil_type = NilType()
nil = Nil()
