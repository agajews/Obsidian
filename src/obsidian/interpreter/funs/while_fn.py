from ..types import (
    Bool,
    PrimFun,
    Panic,
    nil,
)
from ..types.ast import ASTList
from ..types.scope import type_name


def check_condition(condition, scope):
    res = scope.eval(condition)
    if not isinstance(res, Bool):
        raise Panic('Conditions passed to `prim.while` must return `Bool`s, not `{}`'.format(
            type_name(res)))
    return res.bool


class While(PrimFun):
    def __init__(self):
        super().__init__('prim.while', ['cond', 'body'])

    def macro(self, scope, condition, body):
        self.typecheck_arg(body, ASTList)
        statements = body.elems_list()
        while check_condition(condition, scope):
            for statement in statements:
                scope.eval(statement)
        return nil


while_fn = While()
