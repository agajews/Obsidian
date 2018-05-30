from ..types import (
    Panic,
    PrimFun,
    Fun,
    String,
    List,
)


class FunConstructor(PrimFun):
    def __init__(self):
        super().__init__('Fun', variadic=True)

    def macro(self, scope, *args):
        if len(args) < 2:
            raise Panic(
                'PrimFun `Fun` requires a name and at least one body statement as arguments, not `{}` arguments'.format(len(args)))
        name = args[0]
        name = scope.eval(name)
        self.typecheck_arg(name, String)
        body = args[1:]
        return Fun(scope, name, List(body))


class FunToStr(PrimFun):
    def __init__(self):
        super().__init__('Fun.to_str', ['fun'])

    def fun(self, fun):
        self.typecheck_arg(fun, Fun)
        return String('<Fun `{}`>'.format(fun.name_string()))


Fun.T.set('call', FunConstructor())
Fun.T.get('methods').set('to_str', FunToStr())
