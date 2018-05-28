from ..types import (
    Tuple,
    Bool,
    PrimFun,
    Panic,
    nil
)
from ..types.ast import ASTTuple


class Cond(PrimFun):
    def __init__(self):
        super().__init__('cond', variadic=True)

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
            condition, expr = elems.elems
            condition = scope.eval(condition)
            if not isinstance(condition, Bool):
                raise Panic('Conditions must return Bools')
            if condition.bool:
                return scope.eval(expr)
        return nil


cond = Cond()
