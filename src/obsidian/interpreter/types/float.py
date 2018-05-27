from ..bootstrap import (
    Panic, Object, Type, PrimFun,
    object_type,
    String
)


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


class FloatType(Type):
    def __init__(self):
        super().__init__('Float', object_type, ['ast'],
                         methods={'to_str': FloatToStr()})

    def macro(self, scope, ast):
        float = ast.get('float')
        if not isinstance(float, Float):
            raise Panic('Invalid float')
        return Float(float.float)


float_type = FloatType()
