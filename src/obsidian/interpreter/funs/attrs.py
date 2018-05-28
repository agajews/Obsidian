from ..types import (
    PrimFun,
    String,
    List,
)


class Attrs(PrimFun):
    def __init__(self):
        super().__init__('prim.attrs', ['object'])

    def fun(self, obj):
        return List(String(k) for k in obj.attrs.keys())


attrs = Attrs()
