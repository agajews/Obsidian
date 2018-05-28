from ..bootstrap import (
    Panic,
    Object,
    Type,
    PrimFun,
    String,
    object_type,
)


class Float(Object):
    def __init__(self, val):
        super().__init__({}, float_type)
        self.float = val

    def __repr__(self):
        return str(self.float)


class FloatToStr(PrimFun):
    def __init__(self):
        super().__init__('Float.to_str', ['float'])

    def fun(self, float):
        if not isinstance(float, Float):
            raise Panic('Argument must be a float')
        return String(str(float.float))


class FloatType(Type):
    def __init__(self):
        super().__init__('Float', object_type,
                         methods={'to_str': FloatToStr()})


float_type = FloatType()
