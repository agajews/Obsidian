from ..types import (
    PrimFun,
    String,
    Bool,
    Int,
    Symbol,
    true,
    false,
)


class BoolToStr(PrimFun):
    def __init__(self):
        super().__init__('Bool.to_str', ['bool'])

    def fun(self, bool):
        self.typecheck_arg(bool, Bool)
        return String('true' if bool.bool else 'false')


class And(PrimFun):
    def __init__(self):
        super().__init__('bool.and', ['a', 'b'])
        self.set('precedence', Int(3))
        self.set('associativity', Symbol('right'))

    def macro(self, scope, a, b):
        a = scope.eval(a)
        self.typecheck_arg(a, Bool)
        if not a.bool:
            return false
        b = scope.eval(b)
        self.typecheck_arg(b, Bool)
        return b


class Or(PrimFun):
    def __init__(self):
        super().__init__('bool.or', ['a', 'b'])
        self.set('precedence', Int(3))
        self.set('associativity', Symbol('right'))

    def macro(self, scope, a, b):
        a = scope.eval(a)
        self.typecheck_arg(a, Bool)
        if a.bool:
            return true
        b = scope.eval(b)
        self.typecheck_arg(b, Bool)
        return b


Bool.T.get('methods').set('to_str', BoolToStr())
and_fn = And()
or_fn = Or()
