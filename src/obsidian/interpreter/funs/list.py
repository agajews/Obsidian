from ..types import (
    PrimFun,
    Panic,
    List,
    Int,
    String,
    list_type
)
from .get_attr import get_attr


class ListGet(PrimFun):
    def __init__(self):
        super().__init__('get', ['list', 'idx'])

    def fun(self, lst, idx):
        if not isinstance(lst, List):
            raise Panic('List must be a list')
        if not isinstance(idx, Int):
            raise Panic('Index must be an int')
        return lst.elems[idx.int]


class ListToStr(PrimFun):
    def __init__(self):
        super().__init__('to_str', ['list'])

    def macro(self, scope, lst):
        lst = scope.eval(lst)
        if not isinstance(lst, List):
            raise Panic('Argument must be a list')
        strings = [get_attr.fun(elem, String('to_str')).call(scope)
                   for elem in lst.elems]
        for string in strings:
            if not isinstance(string, String):
                raise Panic('to_str must return a string')
        return String('[' + ', '.join(string.str for string in strings) + ']')


list_type.get('methods').set('get', ListGet())
list_type.get('methods').set('to_str', ListToStr())
