from ..types import PrimFun, Panic, String, object_type


class ObjectAssign(PrimFun):
    def __init__(self):
        super().__init__('Object.=', ['object', 'val'])

    def fun(self, obj, val):
        return val


class ObjectToStr(PrimFun):
    def __init__(self):
        super().__init__('Object.to_str', ['object'])

    def fun(self, obj):
        type_name = obj.get('meta').get('type').get('name')
        if not isinstance(type_name, String):
            raise Panic('Invalid type name')
        return String('<{}>'.format(type_name.str))


object_type.get('methods').set('=', ObjectAssign())
object_type.get('methods').set('to_str', ObjectToStr())
