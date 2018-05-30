from ..bootstrap import (
    Object,
    Type,
)


class Symbol(Object):
    T = Type('Symbol', Object.T)

    def __init__(self, symbol):
        super().__init__({})
        self.symbol = symbol

    def __repr__(self):
        return '@{}'.format(self.symbol)
