from ..bootstrap import (
    Panic,
    Object,
    Type,
    PrimFun,
    object_type,
)


class Tuple(Object):
    def __init__(self, elems):
        super().__init__({}, tuple_type)
        self.elems = tuple(elems)

    def __repr__(self):
        return str(self.elems)


class TupleConstructor(PrimFun):
    def __init__(self):
        super().__init__('Tuple', ['ast'])

    def macro(self, scope, ast):
        elems = ast.get('elems')
        if not isinstance(elems, Tuple):
            raise Panic('Invalid tuple')
        return Tuple([scope.eval(elem) for elem in elems.elems])


class TupleType(Type):
    def __init__(self):
        super().__init__('Tuple', object_type, constructor=TupleConstructor())


tuple_type = TupleType()
