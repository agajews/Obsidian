from ..bootstrap import (
    PrimFun,
    Panic,
)
from ..types import Map, List, Tuple, map_type
from .get_attr import get_attr


class MapConstructor(PrimFun):
    def __init__(self):
        super().__init__('Map', ['ast'])

    def macro(self, scope, ast):
        ast = scope.eval(ast)
        elems = ast.get('elems')
        if not isinstance(elems, List):
            raise Panic('Invalid map')
        dictionary = {}
        for elem in elems.elems:
            if not isinstance(elem, Tuple):
                raise Panic('Arguments to map must be tuples')
            if not len(elem.elems) == 2:
                raise Panic('Arguments to map must be pairs')
            key, value = elem.elems
            hash_code = get_attr.fun(key, 'hash').call(scope)
            dictionary[hash_code] = Tuple((key, value))
        return Map(dictionary)


map_type.set('call', MapConstructor())
