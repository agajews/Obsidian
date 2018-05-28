from ..types import (
    Map,
    List,
    Tuple,
    String,
    Int,
    PrimFun,
    Panic,
    map_type
)
from .get_attr import get_attr


def compute_hash(key, scope):
    hash_code = get_attr.fun(key, String('hash')).call(scope)
    if not isinstance(hash_code, Int):
        raise Panic('hash must return an int')
    return hash_code.int


class MapConstructor(PrimFun):
    def __init__(self):
        super().__init__('Map', ['ast'])

    def macro(self, scope, ast):
        elems = ast.get('elems')
        if not isinstance(elems, List):
            raise Panic('Invalid map')
        dictionary = {}
        for elem in elems.elems:
            elem = scope.eval(elem)
            if not isinstance(elem, Tuple):
                raise Panic('Arguments to map must be tuples')
            if not len(elem.elems) == 2:
                raise Panic('Arguments to map must be pairs')
            key, value = elem.elems
            dictionary[compute_hash(key, scope)] = (key, value)
        return Map(dictionary)


class MapGet(PrimFun):
    def __init__(self):
        super().__init__('get', ['map', 'idx'])

    def macro(self, scope, map, key):
        map = scope.eval(map)
        key = scope.eval(key)
        if not isinstance(map, Map):
            raise Panic('Map must be a map')
        hash_code = compute_hash(key, scope)
        if hash_code not in map.elems:
            raise Panic('No such key in map')
        return map.elems[hash_code][1]


class MapToStr(PrimFun):
    def __init__(self):
        super().__init__('to_str', ['map'])

    def macro(self, scope, map):
        map = scope.eval(map)
        if not isinstance(map, Map):
            raise Panic('Argument must be a map')
        strings = [(get_attr.fun(key, String('to_str')).call(scope),
                    get_attr.fun(val, String('to_str')).call(scope))
                   for hash_code, (key, val) in map.elems.items()]
        for key_str, val_str in strings:
            if not isinstance(key_str, String) or not isinstance(val_str, String):
                raise Panic('to_str must return a string')
        return String('{' + ', '.join('{} -> {}'.format(key_str.str, val_str.str)
                                      for key_str, val_str in strings)
                      + '}')


map_type.set('call', MapConstructor())
map_type.get('methods').set('to_str', MapToStr())
map_type.get('methods').set('get', MapGet())
