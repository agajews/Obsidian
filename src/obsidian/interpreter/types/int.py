from ..bootstrap import (
    Object,
    Type,
)


class Int(Object):
    T = Type('Int', Object.T)

    def __init__(self, val):
        super().__init__({})
        self.int = val

    def __repr__(self):
        return 'Int({})'.format(str(self.int))
