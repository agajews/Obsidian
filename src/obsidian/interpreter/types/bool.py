from ..bootstrap import (
    Object,
    Type,
)


class Bool(Object):
    T = Type('Bool', Object.T)

    def __init__(self, val):
        super().__init__({})
        self.bool = val

    def __repr__(self):
        return 'true' if self.bool else 'false'


true = Bool(True)
false = Bool(False)
