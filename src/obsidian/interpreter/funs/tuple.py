from ..types import (
    PrimFun,
    Panic,
    Tuple,
    Int,
    String,
)
from .get_attr import get_attr
from ..types.scope import to_str
from ..types.ast import ASTTuple


class TupleConstructor(PrimFun):
    def __init__(self):
        super().__init__('Tuple', ['ast'])

    def macro(self, scope, ast):
        self.typecheck_arg(ast, ASTTuple)
        ast.validate()
        return Tuple([scope.eval(elem) for elem in ast.elems_list()])


class TupleToStr(PrimFun):
    def __init__(self):
        super().__init__('Tuple.to_str', ['tuple'])

    def macro(self, scope, tup):
        tup = scope.eval(tup)
        self.typecheck_arg(tup, Tuple)
        strs = [to_str(scope, elem) for elem in tup.elems]
        return String('(' + ', '.join(strs) + ')')


class TupleHash(PrimFun):
    def __init__(self):
        super().__init__('Tuple.hash', ['tuple'])

    def macro(self, scope, tuple):
        tuple = scope.eval(tuple)
        self.typecheck_arg(tuple, Tuple)
        return Int(hash(tuple(get_attr.fun(elem, 'hash').call(scope) for elem in tuple.elems)))


class TupleGet(PrimFun):
    def __init__(self):
        super().__init__('Tuple.get', ['tup', 'idx'])

    def fun(self, tup, idx):
        self.typecheck_arg(tup, Tuple)
        self.typecheck_arg(idx, Int)
        if idx.int >= len(tup.elems):
            raise Panic('Index `{}` out of range (len = `{}`)'.format(
                idx.int, len(tup.elems)))
        return tup.elems[idx.int]


Tuple.T.set('call', TupleConstructor())
Tuple.T.get('methods').set('get', TupleGet())
Tuple.T.get('methods').set('to_str', TupleToStr())
Tuple.T.get('methods').set('hash', TupleHash())
