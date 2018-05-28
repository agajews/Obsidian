from ..types import (
    Map,
    List,
    Tuple,
    String,
    Int,
    PrimFun,
    Panic,
    Bool,
    Scope,
    map_type,
)
from ..types.ast import ASTIdent
from .get_attr import get_attr


class MapKey:
    def __init__(self, key, scope):
        self.key = key
        self.scope = scope

    def __hash__(self):
        hash_code = get_attr.fun(self.key, String('hash')).call(self.scope)
        if not isinstance(hash_code, Int):
            raise Panic('hash must return an int')
        return hash_code.int

    def __eq__(self, other):
        scope = Scope(self.scope)
        scope.set('__other__', other.key)
        res = get_attr.fun(self.key, String('eq')).call(
            scope, [ASTIdent(String('__other__'))])
        if not isinstance(res, Bool):
            raise Panic('eq must return a bool')
        return res.bool


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
        strings = [(get_attr.fun(map_key.key, String('to_str')).call(scope),
                    get_attr.fun(val, String('to_str')).call(scope))
                   for map_key, val in map.elems.items()]
        for key_str, val_str in strings:
            if not isinstance(key_str, String) or not isinstance(val_str, String):
                raise Panic('to_str must return a string')
        return String('{' + ', '.join('{} -> {}'.format(key_str.str, val_str.str)
                                      for key_str, val_str in strings)
                      + '}')


map_type.set('call', MapConstructor())
map_type.get('methods').set('to_str', MapToStr())
map_type.get('methods').set('get', MapGet())
map_type.get('methods').set('set', MapSet())
