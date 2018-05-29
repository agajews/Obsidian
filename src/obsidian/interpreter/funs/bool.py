from ..types import (
    PrimFun,
    Panic,
    Bool,
    Int,
    Symbol,
    true,
    false,
)


class And(PrimFun):
    def __init__(self):
        super().__init__('bool.and', ['a', 'b'])
        self.set('precedence', Int(3))
        self.set('associativity', Symbol('right'))

    def fun(self, a, b):
        if not isinstance(a, Bool):
            raise Panic('Argument `a` must be an int')
        if not isinstance(b, Bool):
            raise Panic('Argument `b` must be an int')
        return Bool(a.bool and b.bool)


class Or(PrimFun):
    def __init__(self):
        super().__init__('bool.or', ['a', 'b'])
        self.set('precedence', Int(3))
        self.set('associativity', Symbol('right'))

    def fun(self, a, b):
        if not isinstance(a, Bool):
            raise Panic('Argument `a` must be an int')
        if not isinstance(b, Bool):
            raise Panic('Argument `b` must be an int')
        return Bool(a.bool or b.bool)


and_fn = And()
or_fn = Or()
