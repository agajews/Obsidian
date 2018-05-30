from ..types import (
    PrimFun,
    true,
    false,
)


class IsFun(PrimFun):
    def __init__(self):
        super().__init__('prim.is', ['a', 'b'])

    def fun(self, a, b):
        return true if a is b else false


is_fn = IsFun()
