from ..types import (
    Map,
    List,
    Tuple,
    String,
    PrimFun,
    Panic,
    map_type
)
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


class MapGet(PrimFun):
    def __init__(self):
        super().__init__('get', ['list', 'idx'])

    def fun(self, lst, idx):
        if not isinstance(lst, List):
            raise Panic('List must be a list')
        if not isinstance(idx, Int):
            raise Panic('Index must be a list')
        return lst.elems[idx.int]


class MapToStr(PrimFun):
    def __init__(self):
        super().__init__('to_str', ['map'])

    def macro(self, scope, map):
        map = scope.eval(map)
        if not isinstance(map, Map):
            raise Panic('Argument must be a map')
        strings = [(get_attr.fun(key, String('to_str')).call(scope),
                    get_attr.fun(val, String('to_str')).call(scope))
                   for key, val in map.elems]
        for key_str, val_str in strings:
            if not isinstance(key_str, String) or not isinstance(val_str, String):
                raise Panic('to_str must return a string')
        return String('{' + ', '.join('{} -> {}'.format(key_str.str, val_str.str)
                                      for key_str, val_str in strings)
                      + '}')


map_type.set('call', MapConstructor())
map_type.get('methods').set('to_str', MapToStr())
