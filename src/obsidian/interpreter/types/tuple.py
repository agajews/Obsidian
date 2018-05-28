from ..bootstrap import (
    Panic,
    Object,
    Type,
    object_type,
)


class Tuple(Object):
    def __init__(self, elems):
        super().__init__({}, tuple_type)
        self.elems = elems

    def __repr__(self):
        return str(self.elems)


class TupleType(Type):
    def __init__(self):
        super().__init__('Tuple', object_type, ['ast'])

    def macro(self, scope, ast):
        elems = ast.get('elems')
        if not isinstance(elems, Tuple):
            raise Panic('Invalid tuple')
        return Tuple([scope.eval(elem) for elem in elems.elems])


tuple_type = TupleType()
