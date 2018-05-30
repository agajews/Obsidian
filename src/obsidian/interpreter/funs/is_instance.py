from ..types import (
    PrimFun,
    true,
    false
)


class IsInstance(PrimFun):
    def __init__(self):
        super().__init__('prim.is_instance', ['obj', 'attr'])

    def fun(self, obj, t):
        return true if obj.get('meta').get('type') is t else false


is_instance = IsInstance()
