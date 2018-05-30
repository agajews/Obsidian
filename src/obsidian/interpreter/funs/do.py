from ..types import PrimFun, Panic


class Do(PrimFun):
    def __init__(self):
        super().__init__('prim.do', variadic=True)

    def macro(self, scope, *body):
        if len(body) == 0:
            raise Panic('PrimFun `prim.do` needs at least one clause')
        for expr in body[:-1]:
            scope.eval(expr)
        return scope.eval(body[-1])


do = Do()
