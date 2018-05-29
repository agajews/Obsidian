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

    def macro(self, scope, a, b):
        a = scope.eval(a)
        if not isinstance(a, Bool):
            raise Panic('Argument `a` must be a bool')
        if not a.bool:
            return false
        b = scope.eval(b)
        if not isinstance(b, Bool):
            raise Panic('Argument `b` must be a bool')
        return b


class Or(PrimFun):
    def __init__(self):
        super().__init__('bool.or', ['a', 'b'])
        self.set('precedence', Int(3))
        self.set('associativity', Symbol('right'))

    def macro(self, scope, a, b):
        a = scope.eval(a)
        if not isinstance(a, Bool):
            raise Panic('Argument `a` must be a bool')
        if a.bool:
            return true
        b = scope.eval(b)
        if not isinstance(b, Bool):
            raise Panic('Argument `b` must be a bool')
        return b


and_fn = And()
or_fn = Or()
