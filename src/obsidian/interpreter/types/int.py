from ..bootstrap import (
    Panic,
    Object,
    Type,
    PrimFun,
    object_type,
    String
)


class Int(Object):
    def __init__(self, val):
        super().__init__({}, int_type)
        self.int = val

    def __repr__(self):
        return 'Int({})'.format(str(self.int))


class IntToStr(PrimFun):
    def __init__(self):
        super().__init__('to_str', ['int'])

    def fun(self, int):
        if not isinstance(int, Int):
            raise Panic('Argument must be an int')
        return String(str(int.int))


class IntHash(PrimFun):
    def __init__(self):
        super().__init__('hash', ['int'])

    def fun(self, int):
        if not isinstance(int, Int):
            raise Panic('Argument must be an int')
        return Int(hash(int.int))


class IntType(Type):
    def __init__(self):
        super().__init__('Int', object_type, ['ast'],
                         methods={'to_str': IntToStr(),
                                  'hash': IntHash()})

    def macro(self, scope, ast):
        int = ast.get('int')
        if not isinstance(int, Int):
            raise Panic('Invalid int')
        return Int(int.int)


int_type = IntType()
