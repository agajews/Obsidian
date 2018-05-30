from ..bootstrap import (
    Object,
    Type,
)


class Tuple(Object):
    T = Type('Tuple', Object.T)

    def __init__(self, elems):
        super().__init__({})
        self.elems = tuple(elems)

    def __repr__(self):
        return str(self.elems)
