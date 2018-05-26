from ..bootstrap import (
    String,
    Type,
)

from .scope import Scope, scope_type


class ModuleType(Type):
    def __init__(self):
        super().__init__('Module', scope_type, ['name', 'parent'])

    def fun(self, name, parent):
        if parent is nil:
            return Module(name)
        return Module(name, parent)


class Module(Scope):
    def __init__(self, name, parent=None, attrs=None):
        super().__init__(parent=parent)
        self.get('meta').set('type', module_type)
        if attrs is not None:
            self.attrs.update(attrs)
        self.get('meta').set('name', String(name))
        self.get('meta').set('module', self)
        # self.set('self', self)


module_type = ModuleType()
