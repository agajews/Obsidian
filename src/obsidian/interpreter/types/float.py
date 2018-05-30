from ..bootstrap import (
    Object,
    Type,
)


class Float(Object):
    T = Type('Float', Object.T)

    def __init__(self, val):
        super().__init__({})
        self.float = val

    def __repr__(self):
        return str(self.float)
