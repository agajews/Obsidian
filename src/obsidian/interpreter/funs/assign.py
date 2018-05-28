from ..types import PrimFun, Panic, String
from .get_attr import get_attr


class Assign(PrimFun):
    def __init__(self):
        super().__init__('prim.assign', ['name', 'val'])

    def macro(self, scope, name, val):
        name = scope.eval(name)
        if not isinstance(name, String):
            raise Panic('Name must be a string')
        name = name.str
        new_val = get_attr.fun(scope.get_recursive(
            name), String('=')).call(scope, [val])
        scope.assign_recursive(name, new_val)
        return new_val


assign = Assign()
