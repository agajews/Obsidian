from ..types import (
    PrimFun,
    Panic,
    Tuple,
    Int,
    String,
    tuple_type,
)
from .get_attr import get_attr
from ..types.scope import to_str


class TupleHash(PrimFun):
    def __init__(self):
        super().__init__('Tuple.hash', ['tuple'])

    def macro(self, scope, tuple):
        tuple = scope.eval(tuple)
        if not isinstance(tuple, Tuple):
            raise Panic('Argument must be a tuple')
        return Int(hash(tuple(get_attr.fun(elem, 'hash').call(scope) for elem in tuple.elems)))


class TupleGet(PrimFun):
    def __init__(self):
        super().__init__('Tuple.get', ['tup', 'idx'])

    def fun(self, tup, idx):
        if not isinstance(tup, Tuple):
            raise Panic('Tuple must be a tuple')
        if not isinstance(idx, Int):
            raise Panic('Index must be an int')
        if idx.int >= len(tup.elems):
            raise Panic('Index out of range')
        return tup.elems[idx.int]


class TupleToStr(PrimFun):
    def __init__(self):
        super().__init__('Tuple.to_str', ['tuple'])

    def macro(self, scope, tup):
        tup = scope.eval(tup)
        if not isinstance(tup, Tuple):
            raise Panic('Argument must be a tuple')
        strs = [to_str(scope, elem) for elem in tup.elems]
        return String('(' + ', '.join(strs) + ')')


tuple_type.get('methods').set('get', TupleGet())
tuple_type.get('methods').set('to_str', TupleToStr())
tuple_type.get('methods').set('hash', TupleHash())
