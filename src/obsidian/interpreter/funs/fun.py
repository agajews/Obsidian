from ..types import (
    PrimFun,
    Fun,
    String,
)


class FunConstructor(PrimFun):
    def __init__(self):
        super().__init__('Fun', ['name', 'body'])

    def macro(self, scope, name, body):
        name = scope.eval(name)
        return Fun(scope, name, body)


class FunToStr(PrimFun):
    def __init__(self):
        super().__init__('Fun.to_str', ['fun'])

    def fun(self, fun):
        self.typecheck_arg(fun, Fun)
        return String('<Fun `{}`>'.format(fun.name_string()))


Fun.T.set('call', FunConstructor())
Fun.T.get('methods').set('to_str', FunToStr())
