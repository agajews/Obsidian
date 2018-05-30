from ..types import (
    Map,
    Tuple,
    String,
    PrimFun,
    Panic,
)
from ..types.scope import (
    to_str,
    hash_obj,
    obj_eq,
    type_name,
    call_method,
)
from ..types.ast import ASTMap, ASTIdent, ASTList
from .get_attr import get_attr


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
        self.typecheck_arg(ast, ASTMap)
        ast.validate()
        dictionary = {}
        elems = ast.get('elems').elems
        for elem in elems:
            elem = scope.eval(elem)
            if not isinstance(elem, Tuple):
                raise Panic(
                    'Elements in `Map` must be `Tuple`s, not `{}`'.format(type_name(elem)))
            if not len(elem.elems) == 2:
                raise Panic('Elements in `Map` must be `Tuple`s of length `2`, not `{}`'.format(
                    len(elem.elems)))
            key, value = elem.elems
            key = MapKey(key, scope)
            dictionary[key] = value
        return Map(dictionary)


class MapGet(PrimFun):
    def __init__(self):
        super().__init__('Map.get', ['map', 'key'])

    def macro(self, scope, map, key):
        map = scope.eval(map)
        self.typecheck_arg(map, Map)
        key = scope.eval(key)
        map_key = MapKey(key, scope)
        if map_key not in map.elems:
            raise Panic('No such key `{}` in `Map`'.format(to_str(scope, key)))
        return map.elems[map_key]


class MapSet(PrimFun):
    def __init__(self):
        super().__init__('Map.set', ['map', 'key', 'val'])

    def macro(self, scope, map, key, val):
        map = scope.eval(map)
        self.typecheck_arg(map, Map)
        key = scope.eval(key)
        val = scope.eval(val)
        key = MapKey(key, scope)
        map.elems[key] = val


class MapToStr(PrimFun):
    def __init__(self):
        super().__init__('Map.to_str', ['map'])

    def macro(self, scope, map):
        map = scope.eval(map)
        self.typecheck_arg(map, Map)
        strs = [(to_str(scope, map_key.key), to_str(scope, val))
                for map_key, val in map.elems.items()]
        return String('{' + ', '.join('{} -> {}'.format(key_str, val_str)
                                      for key_str, val_str in strs)
                      + '}')


class MapDot(PrimFun):
    def __init__(self):
        super().__init__('Map.dot', ['map', 'attr'])

    def macro(self, scope, map, attr):
        map = scope.eval(map)
        attr = scope.eval(attr)
        self.typecheck_arg(map, Map)
        self.typecheck_arg(attr, (ASTIdent, ASTList))
        attr.validate()
        if isinstance(attr, ASTIdent):
            return get_attr.fun(map, attr.get('ident'))
        else:
            elems = attr.elems_list()
            if not len(elems) == 1:
                raise Panic(
                    'PrimFun `Map.dot` needs exactly `1` element in its attribute list, not `{}`'
                    .format(len(elems)))
            return call_method(scope, map, 'get', [attr.elems_list()[0]])


Map.T.set('call', MapConstructor())
Map.T.get('methods').set('to_str', MapToStr())
Map.T.get('methods').set('get', MapGet())
Map.T.get('methods').set('set', MapSet())
Map.T.get('methods').set('dot', MapDot())
