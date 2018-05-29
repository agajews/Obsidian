from ..types import (
    Map,
    List,
    Tuple,
    String,
    PrimFun,
    Panic,
    map_type,
)
from ..types.scope import to_str, hash_obj, obj_eq


class MapKey:
    def __init__(self, key, scope):
        self.key = key
        self.scope = scope

    def __hash__(self):
        return hash_obj(self.scope, self.key)

    def __eq__(self, other):
        return obj_eq(self.scope, self.key, other)


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
            key = MapKey(key, scope)
            dictionary[key] = value
        return Map(dictionary)


class MapGet(PrimFun):
    def __init__(self):
        super().__init__('Map.get', ['map', 'key'])

    def macro(self, scope, map, key):
        map = scope.eval(map)
        key = scope.eval(key)
        if not isinstance(map, Map):
            raise Panic('Map must be a map')
        key = MapKey(key, scope)
        if key not in map.elems:
            raise Panic('No such key in map')
        return map.elems[key]


class MapSet(PrimFun):
    def __init__(self):
        super().__init__('Map.set', ['map', 'key', 'val'])

    def macro(self, scope, map, key, val):
        map = scope.eval(map)
        key = scope.eval(key)
        val = scope.eval(val)
        if not isinstance(map, Map):
            raise Panic('Map must be a map')
        key = MapKey(key, scope)
        map.elems[key] = val


class MapToStr(PrimFun):
    def __init__(self):
        super().__init__('Map.to_str', ['map'])

    def macro(self, scope, map):
        map = scope.eval(map)
        if not isinstance(map, Map):
            raise Panic('Argument must be a map')
        strs = [(to_str(scope, map_key.key), to_str(scope, val))
                for map_key, val in map.elems.items()]
        return String('{' + ', '.join('{} -> {}'.format(key_str, val_str)
                                      for key_str, val_str in strs)
                      + '}')


map_type.set('call', MapConstructor())
map_type.get('methods').set('to_str', MapToStr())
map_type.get('methods').set('get', MapGet())
map_type.get('methods').set('set', MapSet())
