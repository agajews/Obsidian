from ..types import (
    PrimFun,
)


class Type(PrimFun):
    def __init__(self):
        super().__init__('prim.type', ['obj'])

    def fun(self, obj):
        # print('Calling type')
        # print(obj)
        # print({k: v for k, v in obj.get('meta').attrs.items() if k != 'meta'})
        # print(obj.get('meta').get('type'))
        return obj.get('meta').get('type')


type_fn = Type()
