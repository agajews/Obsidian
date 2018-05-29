from ..types import (
    PrimFun,
    Panic,
    List,
    Int,
    String,
    list_type
)
from ..types.scope import to_str


class ListGet(PrimFun):
    def __init__(self):
        super().__init__('List.get', ['list', 'idx'])

    def fun(self, lst, idx):
        if not isinstance(lst, List):
            raise Panic('List must be a list')
        if not isinstance(idx, Int):
            raise Panic('Index must be an int')
        if idx.int >= len(lst.elems):
            raise Panic('Index `{}` out of range'.format(idx.int))
        return lst.elems[idx.int]


class ListSet(PrimFun):
    def __init__(self):
        super().__init__('List.set', ['list', 'idx', 'val'])

    def fun(self, lst, idx, val):
        if not isinstance(lst, List):
            raise Panic('List must be a list')
        if not isinstance(idx, Int):
            raise Panic('Index must be an int')
        if idx.int >= len(lst.elems):
            raise Panic('Index `{}` out of range'.format(idx.int))
        lst.elems[idx.int] = val


class ListToStr(PrimFun):
    def __init__(self):
        super().__init__('List.to_str', ['list'])

    def macro(self, scope, lst):
        lst = scope.eval(lst)
        if not isinstance(lst, List):
            raise Panic('Argument must be a list')
        strs = [to_str(scope, elem) for elem in lst.elems]
        return String('[' + ', '.join(strs) + ']')


class ListLen(PrimFun):
    def __init__(self):
        super().__init__('List.len', ['list'])

    def fun(self, lst):
        if not isinstance(lst, List):
            raise Panic('Argument must be a list')
        return Int(len(lst.elems))


list_type.get('methods').set('len', ListLen())
list_type.get('methods').set('get', ListGet())
list_type.get('methods').set('set', ListSet())
list_type.get('methods').set('to_str', ListToStr())
