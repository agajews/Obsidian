from ..types import (
    PrimFun,
    Module,
    String,
    nil,
)


class ModuleConstructor(PrimFun):
    def __init__(self):
        super().__init__('Module', ['name', 'parent'])

    def fun(self, name, parent):
        if parent is nil:
            return Module(name)
        return Module(name, parent)


class ModuleToStr(PrimFun):
    def __init__(self):
        super().__init__('Module.to_str', ['module'])

    def fun(self, module):
        self.typecheck_arg(module, Module)
        return String('<Module `{}`>'.format(module.name_string()))


Module.T.set('call', ModuleConstructor())
Module.T.get('methods').set('to_str', ModuleToStr())
