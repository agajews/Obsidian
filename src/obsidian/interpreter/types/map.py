from ..bootstrap import (
    Object,
    Type,
)


class Map(Object):
    T = Type('Map', Object.T)

    def __init__(self, elems):
        super().__init__({})
        self.elems = elems

    def __repr__(self):
        return str(self.elems)
