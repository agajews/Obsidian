from ..types import PrimFun, Panic, String


class Let(PrimFun):
    def __init__(self):
        super().__init__('let', ['name', 'val'])

    def macro(self, scope, name, val):
        name = scope.eval(name)
        val = scope.eval(val)
        if not isinstance(name, String):
            raise Panic('Name must be a string')
        return scope.set(name.str, val)


let = Let()
