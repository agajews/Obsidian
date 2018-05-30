from ..types import (
    Bool,
    PrimFun,
    Panic,
    nil,
)
from ..types.scope import type_name


def check_condition(condition, scope):
    res = scope.eval(condition)
    if not isinstance(res, Bool):
        raise Panic('Conditions passed to `prim.while` must return `Bool`s, not `{}`'.format(
            type_name(res)))
    return res.bool


class While(PrimFun):
    def __init__(self):
        super().__init__('prim.while', variadic=True)

    def macro(self, scope, *args):
        if len(args) < 2:
            raise Panic(
                'PrimFun `Fun` requires a name and at least one body statement as arguments, not `{}` arguments'.format(len(args)))
        condition = args[0]
        statements = args[1:]
        res = nil
        while check_condition(condition, scope):
            for statement in statements:
                res = scope.eval(statement)
        return res


while_fn = While()
