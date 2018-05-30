from ..types import String, PrimFun


class SetAttr(PrimFun):
    def __init__(self):
        super().__init__('set_attr', ['obj', 'attr', 'val'])

    def fun(self, obj, attr, val):
        self.typecheck_arg(attr, String)
        return obj.set(attr.str, val)


set_attr = SetAttr()
