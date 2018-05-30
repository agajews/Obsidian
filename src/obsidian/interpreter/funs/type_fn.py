from ..types import (
    PrimFun,
)


class Type(PrimFun):
    def __init__(self):
        super().__init__('prim.type', ['obj'])

    def fun(self, obj):
        return obj.get('meta').get('type')


type_fn = Type()
