from ..types import PrimFun, Panic, String


class PanicFun(PrimFun):
    def __init__(self):
        super().__init__('prim.panic', ['message'])

    def fun(self, message):
        if not isinstance(message, String):
            raise Panic('Panic message must be a string')
        raise Panic(message.str)


panic = PanicFun()
