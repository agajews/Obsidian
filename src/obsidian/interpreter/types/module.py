from ..bootstrap import (
    String,
    Type,
)

from .scope import Scope


class Module(Scope):
    T = Type('Module', Scope.T)

    def __init__(self, name, parent=None, attrs=None):
        super().__init__(parent=parent)
        if attrs is not None:
            self.attrs.update(attrs)
        self.get('meta').set('name', String(name))
        self.get('meta').set('module', self)
