from ..bootstrap import (
    Panic,
    Object, Type,
    object_type,
)


class List(Object):
    def __init__(self, elems):
        super().__init__({}, list_type)
        self.elems = elems

    def __repr__(self):
        return str(self.elems)


class ListType(Type):
    def __init__(self):
        super().__init__('List', object_type, ['ast'])

    def macro(self, scope, ast):
        elems = ast.get('elems')
        if not isinstance(elems, List):
            raise Panic('Invalid list')
        return List([scope.eval(elem) for elem in elems.elems])


list_type = ListType()
