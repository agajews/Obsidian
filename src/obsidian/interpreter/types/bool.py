from ..bootstrap import (
    Panic,
    Object,
    Type,
    PrimFun,
    String,
    object_type,
)


class Bool(Object):
    def __init__(self, val):
        super().__init__({}, bool_type)
        self.bool = val

    def __repr__(self):
        return 'true' if self.bool else 'false'


class BoolToStr(PrimFun):
    def __init__(self):
        super().__init__('Bool.to_str', ['bool'])

    def fun(self, bool):
        if not isinstance(bool, Bool):
            raise Panic('Argument must be a bool')
        return String('true' if bool.bool else 'false')


class BoolType(Type):
    def __init__(self):
        super().__init__('Bool', object_type,
                         methods={'to_str': BoolToStr()})


bool_type = BoolType()
true = Bool(True)
false = Bool(False)
