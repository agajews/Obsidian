from ..types import (
    PrimFun,
    Panic,
    Int,
    String,
    Symbol,
    Map,
    true,
    false,
    int_type,
)
from ..types.ast import ASTString, ASTInt
from .get_attr import get_attr


class IntConstructor(PrimFun):
    def __init__(self):
        super().__init__('Int', ['ast'])

    def macro(self, scope, ast):
        int = ast.get('int')
        if not isinstance(int, Int):
            raise Panic('Invalid int')
        sigil = ast.get('sigil')
        if not isinstance(sigil, String):
            raise Panic('Invalid sigil')
        int = Int(int.int)
        if sigil.str == '':
            return int
        constructors = int_type.get('sigils')
        constructor = get_attr.fun(
            constructors, String('get')).call(scope, [ASTString(sigil)])
        return constructor.call(scope, [ASTInt(int)])


class IntEq(PrimFun):
    def __init__(self):
        super().__init__('Int.eq', ['a', 'b'])

    def fun(self, a, b):
        if not isinstance(a, Int):
            raise Panic('Argument `a` must be an int')
        if not isinstance(b, Int):
            raise Panic('Argument `b` must be an int')
        return true if a.int == b.int else false


class IntHash(PrimFun):
    def __init__(self):
        super().__init__('Int.hash', ['int'])

    def fun(self, int):
        if not isinstance(int, Int):
            raise Panic('Argument must be an int')
        return Int(hash(int.int))


class Add(PrimFun):
    def __init__(self):
        super().__init__('int.add', ['a', 'b'])
        self.set('precedence', Int(6))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        if not isinstance(a, Int):
            raise Panic('Argument `a` must be an int')
        if not isinstance(b, Int):
            raise Panic('Argument `b` must be an int')
        return Int(a.int + b.int)


class Sub(PrimFun):
    def __init__(self):
        super().__init__('int.sub', ['a', 'b'])
        self.set('precedence', Int(6))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        if not isinstance(a, Int):
            raise Panic('Argument `a` must be an int')
        if not isinstance(b, Int):
            raise Panic('Argument `b` must be an int')
        return Int(a.int - b.int)


class Mul(PrimFun):
    def __init__(self):
        super().__init__('int.mul', ['a', 'b'])
        self.set('precedence', Int(7))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        if not isinstance(a, Int):
            raise Panic('Argument `a` must be an int')
        if not isinstance(b, Int):
            raise Panic('Argument `b` must be an int')
        return Int(a.int * b.int)


class FloorDiv(PrimFun):
    def __init__(self):
        super().__init__('int.floor_div', ['a', 'b'])
        self.set('precedence', Int(7))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        if not isinstance(a, Int):
            raise Panic('Argument `a` must be an int')
        if not isinstance(b, Int):
            raise Panic('Argument `b` must be an int')
        return Int(a.int // b.int)


class Mod(PrimFun):
    def __init__(self):
        super().__init__('int.mod', ['a', 'b'])
        self.set('precedence', Int(7))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        if not isinstance(a, Int):
            raise Panic('Argument `a` must be an int')
        if not isinstance(b, Int):
            raise Panic('Argument `b` must be an int')
        return Int(a.int % b.int)


class Pow(PrimFun):
    def __init__(self):
        super().__init__('int.pow', ['a', 'b'])
        self.set('precedence', Int(8))
        self.set('associativity', Symbol('right'))

    def fun(self, a, b):
        if not isinstance(a, Int):
            raise Panic('Argument `a` must be an int')
        if not isinstance(b, Int):
            raise Panic('Argument `b` must be an int')
        return Int(a.int ** b.int)


class Eq(PrimFun):
    def __init__(self):
        super().__init__('int.eq', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Int):
                raise Panic('Argument {} must be an int'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a.int != b.int:
                return false
        return true


class NEq(PrimFun):
    def __init__(self):
        super().__init__('int.eq', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Int):
                raise Panic('Argument {} must be an int'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a.int == b.int:
                return false
        return true


class LT(PrimFun):
    def __init__(self):
        super().__init__('int.lt', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Int):
                raise Panic('Argument {} must be an int'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a.int >= b.int:
                return false
        return true


class LTE(PrimFun):
    def __init__(self):
        super().__init__('int.lte', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Int):
                raise Panic('Argument {} must be an int'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a.int > b.int:
                return false
        return true


class GT(PrimFun):
    def __init__(self):
        super().__init__('int.gt', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Int):
                raise Panic('Argument {} must be an int'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a.int <= b.int:
                return false
        return true


class GTE(PrimFun):
    def __init__(self):
        super().__init__('int.gte', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Int):
                raise Panic('Argument {} must be an int'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a.int < b.int:
                return false
        return true


int_type.set('call', IntConstructor())
int_type.get('methods').set('eq', IntEq())
int_type.get('methods').set('hash', IntHash())
int_type.set('sigils', Map({}))

add = Add()
sub = Sub()
mul = Mul()
floor_div = FloorDiv()
mod = Mod()
pow = Pow()
eq = Eq()
neq = NEq()
lt = LT()
lte = LTE()
gt = GT()
gte = GTE()
