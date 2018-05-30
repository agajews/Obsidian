from ..types import (
    PrimFun,
    Panic,
    String,
)


class PanicFun(PrimFun):
    def __init__(self):
        super().__init__('prim.panic', ['message'])

    def fun(self, message):
        self.typecheck_arg(message, String)
        raise Panic(message.str)


panic = PanicFun()
