from ..bootstrap import (
    Panic,
    Object,
    Type,
    object_type,
)
from .list import List
from .tuple import Tuple


class Map(Object):
    def __init__(self, elems):
        super().__init__({}, map_type)
        self.elems = elems

    def __repr__(self):
        return str(self.elems)


class MapType(Type):
    def __init__(self):
        super().__init__('Map', object_type, ['ast'])

    def macro(self, caller_scope, ast):
        # ast = caller_scope.eval(ast)
        # elems = ast.get('elems')
        # if not isinstance(elems, List):
        #     raise Panic('Invalid map')
        # dictionary = {}
        # for elem in elems.elems:
        #     if not isinstance(elem, Tuple):
        #         raise Panic('Arguments to map must be tuples')
        #     if not len(elem.elems) == 2:
        #         raise Panic('Arguments to map must be pairs')
        #     key, value = elem.elems
        #     hash_code = scope.get_attr.fun(key, 'hash').call(scope)
        #     dictionary[hash_code] = Tuple((key, value))
        # return Map(dictionary)
        return {}


map_type = MapType()
