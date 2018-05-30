from ..bootstrap import (
    Object,
    Type,
)


class List(Object):
    T = Type('List', Object.T)

    def __init__(self, elems):
        super().__init__({})
        self.elems = elems

    def __repr__(self):
        return str(self.elems)
