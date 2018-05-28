from ..bootstrap import (
    Panic,
    Object,
    Type,
    PrimFun,
    String,
    object_type,
)
from .int import Int


class Float(Object):
    def __init__(self, val):
        super().__init__({}, float_type)
        self.float = val

    def __repr__(self):
        return str(self.float)


class FloatToStr(PrimFun):
    def __init__(self):
        super().__init__('to_str', ['float'])

    def fun(self, float):
        if not isinstance(float, Float):
            raise Panic('Argument must be a float')
        return String(str(float.float))


class FloatHash(PrimFun):
    def __init__(self):
        super().__init__('hash', ['float'])

    def fun(self, float):
        if not isinstance(float, Float):
            raise Panic('Argument must be a float')
        return Int(hash(float.float))


class FloatConstructor(PrimFun):
    def __init__(self):
        super().__init__('Float', ['ast'])

    def macro(self, scope, ast):
        float = ast.get('float')
        if not isinstance(float, Float):
            raise Panic('Invalid float')
        return Float(float.float)


class FloatType(Type):
    def __init__(self):
        super().__init__('Float', object_type,
                         methods={'to_str': FloatToStr(),
                                  'hash': FloatHash()},
                         constructor=FloatConstructor())


float_type = FloatType()
