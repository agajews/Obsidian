from ..bootstrap import (
    Panic, Object, Type, PrimFun,
    object_type,
    String
)


class Bool(Object):
    def __init__(self, val):
        super().__init__({}, bool_type)
        self.bool = val

    def __repr__(self):
        return 'true' if self.bool else 'false'


class BoolToStr(PrimFun):
    def __init__(self):
        super().__init__('to_str', ['bool'])

    def fun(self, bool):
        return String('true' if bool.bool else 'false')


class BoolType(Type):
    def __init__(self):
        super().__init__('Bool', object_type, ['ast'],
                         methods={'to_str': BoolToStr()})

    def macro(self, scope, ast):
        raise Panic('Bools cannot be instantiated')


bool_type = BoolType()
true = Bool(True)
false = Bool(False)
