from ..types import String, PrimFun, Panic, true, false


class HasAttr(PrimFun):
    def __init__(self):
        super().__init__('has_attr', ['obj', 'attr'])

    def fun(self, obj, attr):
        if not isinstance(attr, String):
            raise Panic('Attribute must be a string')
        return true if obj.has(attr.str) else false


has_attr = HasAttr()
