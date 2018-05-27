from ..types import PrimFun, Panic, List, Int


class Get(PrimFun):
    def __init__(self):
        super().__init__('get', ['list', 'idx'])

    def fun(self, lst, idx):
        if not isinstance(lst, List):
            raise Panic('List must be a list')
        if not isinstance(idx, Int):
            raise Panic('Index must be a list')
        return lst.elems[idx.int]


get = Get()
