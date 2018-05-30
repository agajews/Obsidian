from ..types import (
    String,
    PrimFun,
    true,
    false,
)


class HasAttr(PrimFun):
    def __init__(self):
        super().__init__('has_attr', ['obj', 'attr'])

    def fun(self, obj, attr):
        self.typecheck_arg(attr, String)
        return true if obj.has(attr.str) else false


has_attr = HasAttr()
