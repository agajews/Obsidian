from ..types import Tuple, Panic, PrimFun, tuple_type, Int
from ..scope import get_attr


class TupleHash(PrimFun):
    def __init__(self):
        super().__init__('hash', ['tuple'])

    def macro(self, scope, tuple):
        tuple = scope.eval(tuple)
        if not isinstance(tuple, Tuple):
            raise Panic('Argument must be a tuple')
        return Int(hash(tuple(get_attr.fun(elem, 'hash').call(scope) for elem in tuple.elems)))


tuple_type.get('methods').set('hash', TupleHash())
