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
            raise Panic('PrimFun `Cond` needs at least one clause')
        for clause in clauses:
            self.typecheck_arg(clause, ASTTuple)
            elems = clause.elems_list()
            if not len(elems) == 2:
                raise Panic(
                    'PrimFun `Cond` needs clauses to be tuples of length 2, not `{}`'
                    .format(len(elems)))
            condition, exprs = elems
            self.typecheck_arg(exprs, ASTList)
            exprs = exprs.elems_list()
            if len(exprs) == 0:
                raise Panic(
                    'PrimFun `Cond` needs clauses to have at least one expression')
            condition = scope.eval(condition)
            if not isinstance(condition, Bool):
                raise Panic(
                    'PrimFun `Cond` needs conditions to return `Bool`s, not `{}`'.format(type_name(condition)))
            if condition.bool:
                for expr in exprs[:-1]:
                    scope.eval(expr)
                return scope.eval(exprs[-1])
        return nil


cond = Cond()
