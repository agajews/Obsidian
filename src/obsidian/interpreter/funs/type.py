from ..types import (
    PrimFun,
    Type,
    String,
)


class TypeToStr(PrimFun):
    def __init__(self):
        super().__init__('Type.to_str', ['type'])

    def fun(self, t):
        t.typecheck_attr('name', String)
        return String('<Type `{}`>'.format(t.get('name').str))


Type.T.get('methods').set('to_str', TypeToStr())
