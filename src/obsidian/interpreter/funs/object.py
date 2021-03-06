from ..types import (
    Object,
    PrimFun,
    Panic,
    String,
)
from ..types.ast import ASTIdent
from .get_attr import get_attr


class ObjectAssign(PrimFun):
    def __init__(self):
        super().__init__('Object.assign', ['object', 'val'])

    def fun(self, obj, val):
        return val


class ObjectDot(PrimFun):
    def __init__(self):
        super().__init__('Object.dot', ['object', 'scope', 'attr'])

    def fun(self, obj, scope, attr):
        self.typecheck_arg(attr, ASTIdent)
        return get_attr.fun(obj, attr.get('ident'))


class ObjectToStr(PrimFun):
    def __init__(self):
        super().__init__('Object.to_str', ['object'])

    def fun(self, obj):
        type_name = obj.get('meta').get('type').get('name')
        if not isinstance(type_name, String):
            raise Panic('Invalid type name')
        return String('<{}>'.format(type_name.str))


Object.T.get('methods').set('assign', ObjectAssign())
Object.T.get('methods').set('dot', ObjectDot())
Object.T.get('methods').set('to_str', ObjectToStr())
