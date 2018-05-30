from ..types import (
    Bool,
    PrimFun,
    Panic,
    nil,
    type_name,
)
from ..types.ast import ASTTuple, ASTList


class Cond(PrimFun):
    def __init__(self):
        super().__init__('prim.cond', variadic=True)

    def macro(self, scope, *clauses):
        if len(clauses) == 0:
            raise Panic('PrimFun `prim.cond` needs at least one clause')
        for clause in clauses:
            self.typecheck_arg(clause, ASTTuple)
            elems = clause.elems_list()
            if not len(elems) == 2:
                raise Panic(
                    'PrimFun `prim.cond` needs clauses to be tuples of length 2, not `{}`'
                    .format(len(elems)))
            condition, expr = elems
            condition = scope.eval(condition)
            if not isinstance(condition, Bool):
                raise Panic(
                    'PrimFun `prim.cond` needs conditions to return `Bool`s, not `{}`'.format(type_name(condition)))
            if condition.bool:
                return scope.eval(expr)
        return nil


cond = Cond()
