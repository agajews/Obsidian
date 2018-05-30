from ..types import (
    Tuple,
    Bool,
    PrimFun,
    Panic,
    nil,
)
from ..types.ast import ASTTuple, ASTList


class Cond(PrimFun):
    def __init__(self):
        super().__init__('prim.cond', variadic=True)

    def macro(self, scope, *clauses):
        if len(clauses) == 0:
            raise Panic('Cond needs at least one clause')
        for clause in clauses:
            if not isinstance(clause, ASTTuple):
                raise Panic(
                    'Clauses must be tuples of conditions and expressions to evaluate')
            elems = clause.get('elems')
            if not isinstance(elems, Tuple):
                raise Panic('Invalid tuple')
            if not len(elems.elems) == 2:
                raise Panic('Clauses must be tuples of length 2')
            condition, exprs = elems.elems
            if not isinstance(exprs, ASTList):
                raise Panic('Cond expressions must be in a list')
            exprs = exprs.elems_list()
            if len(exprs) == 0:
                raise Panic('Cond clauses must have at least one expression')
            condition = scope.eval(condition)
            if not isinstance(condition, Bool):
                raise Panic('Conditions must return Bools')
            if condition.bool:
                for expr in exprs[:-1]:
                    scope.eval(expr)
                return scope.eval(exprs[-1])
        return nil


cond = Cond()
