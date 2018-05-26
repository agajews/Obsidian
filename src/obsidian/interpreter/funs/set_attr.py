from ..bootstrap import String, PrimFun, Panic


class SetAttr(PrimFun):
    def __init__(self):
        super().__init__('set_attr', ['obj', 'attr', 'val'])

    def fun(self, obj, attr, val):
        if not isinstance(attr, String):
            raise Panic('Attribute must be a string')
        return obj.set(attr.str, val)


set_attr = SetAttr()
