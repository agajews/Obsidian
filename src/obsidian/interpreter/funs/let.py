from ..types import (
    PrimFun,
    Panic,
    String,
)


class Let(PrimFun):
    def __init__(self):
        super().__init__('prim.let', ['name', 'val'])

    def macro(self, scope, name, val):
        # TODO name validation (for operators)
        name = scope.eval(name)
        val = scope.eval(val)
        if not isinstance(name, String):
            raise Panic('Name must be a string')
        # if scope.has(name.str):
        #     raise Panic('Redeclarations are not allowed')
        scope.set(name.str, val)
        return val


let = Let()
