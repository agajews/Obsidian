from ..bootstrap import (
    Object,
    Type,
    object_type,
)


class Map(Object):
    def __init__(self, elems):
        super().__init__({}, map_type)
        self.elems = elems

    def __repr__(self):
        return str(self.elems)


class MapType(Type):
    def __init__(self):
        super().__init__('Map', object_type)


map_type = MapType()
