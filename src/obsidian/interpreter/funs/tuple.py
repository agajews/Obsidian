from ..types import (
    PrimFun,
    Panic,
    Tuple,
    Int,
    String,
    tuple_type,
)
from .get_attr import get_attr


class TupleHash(PrimFun):
    def __init__(self):
        super().__init__('hash', ['tuple'])

    def macro(self, scope, tuple):
        tuple = scope.eval(tuple)
        if not isinstance(tuple, Tuple):
            raise Panic('Argument must be a tuple')
        return Int(hash(tuple(get_attr.fun(elem, 'hash').call(scope) for elem in tuple.elems)))


class Get(PrimFun):
    def __init__(self):
        super().__init__('get', ['tup', 'idx'])

    def fun(self, tup, idx):
        if not isinstance(tup, Tuple):
            raise Panic('Tuple must be a tuple')
        if not isinstance(idx, Int):
            raise Panic('Index must be a list')
        return tup.elems[idx.int]


class TupleToStr(PrimFun):
    def __init__(self):
        super().__init__('Tuple', ['tuple'])

    def macro(self, scope, tup):
        tup = scope.eval(tup)
        if not isinstance(tup, Tuple):
            raise Panic('Argument must be a tuple')
        strings = [get_attr.fun(elem, String('to_str')).call(scope)
                   for elem in tup.elems]
        for string in strings:
            if not isinstance(string, String):
                raise Panic('to_str must return a string')
        return String('(' + ', '.join(string.str for string in strings) + ')')


get = Get()
tuple_type.get('methods').set('to_str', TupleToStr())
tuple_type.get('methods').set('hash', TupleHash())
