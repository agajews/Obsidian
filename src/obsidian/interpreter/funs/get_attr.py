from ..types import Scope, String, PrimFun, Panic
from ..types.ast import ASTIdent


class MethodFun(PrimFun):
    def __init__(self, obj, method):
        super().__init__('method_fun', variadic=True)
        self.obj = obj
        self.method = method

    def macro(self, scope, *args):
        obj_scope = Scope(scope)
        obj_scope.set('__self__', self.obj)
        return self.method.call(obj_scope, [ASTIdent(String('__self__'))] + list(args))


class GetAttr(PrimFun):
    def __init__(self):
        super().__init__('get_attr', ['obj', 'attr'])

    def fun(self, obj, attr):
        if not isinstance(attr, String):
            raise Panic('Attribute must be a string')
        if not obj.has(attr.str):
            obj_type = obj.get('meta').get('type')
            if obj_type.get('methods').has(attr.str):
                return MethodFun(obj, obj_type.get('methods').get(attr.str))
            if obj_type.get('statics').has(attr.str):
                return obj_type.get('statics').get(attr.str)
            while obj_type.get('parent') is not obj_type:
                obj_type = obj_type.get('parent')
                if obj_type.get('methods').has(attr.str):
                    return MethodFun(obj, obj_type.get('methods').get(attr.str))
                if obj_type.get('statics').has(attr.str):
                    return obj_type.get('statics').get(attr.str)
        return obj.get(attr.str)


get_attr = GetAttr()
