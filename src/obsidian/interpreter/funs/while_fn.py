from ..types import (
    List,
    Bool,
    PrimFun,
    Panic,
    nil
)
from ..types.ast import ASTList


def check_condition(condition, scope):
    res = scope.eval(condition)
    if not isinstance(res, Bool):
        raise Panic('Conditions must return Bools')
    return res.bool


class While(PrimFun):
    def __init__(self):
        super().__init__('while', ['cond', 'body'])

    def macro(self, scope, condition, body):
        if not isinstance(body, ASTList):
            raise Panic('Body must be a list of statements')
        statements = body.get('elems')
        if not isinstance(statements, List):
            raise Panic('Invalid ASTList')
        while check_condition(condition, scope):
            for statement in statements.elems:
                scope.eval(statement)
        return nil


while_fn = While()
