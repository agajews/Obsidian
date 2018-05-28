from ..types import (
    PrimFun,
    Panic,
    Int,
    Float,
    Symbol,
    true,
    false,
    float_type,
)


class FloatEq(PrimFun):
    def __init__(self):
        super().__init__('Float.eq', ['a', 'b'])

    def fun(self, a, b):
        if not isinstance(a, Float):
            raise Panic('Argument `a` must be a float')
        if not isinstance(b, Float):
            raise Panic('Argument `b` must be a float')
        return true if a.float == b.float else false


class FloatHash(PrimFun):
    def __init__(self):
        super().__init__('Float.hash', ['float'])

    def fun(self, float):
        if not isinstance(float, Float):
            raise Panic('Argument must be a float')
        return Int(hash(float.float))


class Add(PrimFun):
    def __init__(self):
        super().__init__('float.add', ['a', 'b'])
        self.set('precedence', Int(6))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        if not isinstance(a, Float):
            raise Panic('Argument `a` must be a float')
        if not isinstance(b, Float):
            raise Panic('Argument `b` must be a float')
        return Float(a.float + b.float)


class Sub(PrimFun):
    def __init__(self):
        super().__init__('float.sub', ['a', 'b'])
        self.set('precedence', Int(6))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        if not isinstance(a, Float):
            raise Panic('Argument `a` must be a float')
        if not isinstance(b, Float):
            raise Panic('Argument `b` must be a float')
        return Float(a.float - b.float)


class Mul(PrimFun):
    def __init__(self):
        super().__init__('float.mul', ['a', 'b'])
        self.set('precedence', Int(7))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        if not isinstance(a, Float):
            raise Panic('Argument `a` must be a float')
        if not isinstance(b, Float):
            raise Panic('Argument `b` must be a float')
        return Float(a.float * b.float)


class Div(PrimFun):
    def __init__(self):
        super().__init__('float.div', ['a', 'b'])
        self.set('precedence', Int(7))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        if not isinstance(a, Float):
            raise Panic('Argument `a` must be a float')
        if not isinstance(b, Float):
            raise Panic('Argument `b` must be a float')
        return Float(a.float / b.float)


class FloorDiv(PrimFun):
    def __init__(self):
        super().__init__('float.floor_div', ['a', 'b'])
        self.set('precedence', Int(7))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        if not isinstance(a, Float):
            raise Panic('Argument `a` must be a float')
        if not isinstance(b, Float):
            raise Panic('Argument `b` must be a float')
        return Float(a.float // b.float)


class Mod(PrimFun):
    def __init__(self):
        super().__init__('float.mod', ['a', 'b'])
        self.set('precedence', Int(7))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        if not isinstance(a, Float):
            raise Panic('Argument `a` must be a float')
        if not isinstance(b, Float):
            raise Panic('Argument `b` must be a float')
        return Float(a.float % b.float)


class Pow(PrimFun):
    def __init__(self):
        super().__init__('float.pow', ['a', 'b'])
        self.set('precedence', Int(8))
        self.set('associativity', Symbol('right'))

    def fun(self, a, b):
        if not isinstance(a, Float):
            raise Panic('Argument `a` must be a float')
        if not isinstance(b, Float):
            raise Panic('Argument `b` must be a float')
        return Float(a.float ** b.float)


class Eq(PrimFun):
    def __init__(self):
        super().__init__('float.eq', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Float):
                raise Panic('Argument {} must be a float'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a != b:
                return false
        return true


class NEq(PrimFun):
    def __init__(self):
        super().__init__('float.eq', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Float):
                raise Panic('Argument {} must be a float'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a == b:
                return false
        return true


class LT(PrimFun):
    def __init__(self):
        super().__init__('float.lt', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Float):
                raise Panic('Argument {} must be a float'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a.float >= b.float:
                return false
        return true


class LTE(PrimFun):
    def __init__(self):
        super().__init__('float.lte', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Float):
                raise Panic('Argument {} must be a float'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a.float > b.float:
                return false
        return true


class GT(PrimFun):
    def __init__(self):
        super().__init__('float.gt', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Float):
                raise Panic('Argument {} must be a float'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a.float <= b.float:
                return false
        return true


class GTE(PrimFun):
    def __init__(self):
        super().__init__('float.gte', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            if not isinstance(num, Float):
                raise Panic('Argument {} must be a float'.format(i))
        for a, b in zip(nums[:-1], nums[1:]):
            if a.float < b.float:
                return false
        return true


float_type.get('methods').set('eq', FloatEq())
float_type.get('methods').set('hash', FloatHash())
add = Add()
sub = Sub()
mul = Mul()
div = Div()
floor_div = FloorDiv()
mod = Mod()
pow = Pow()
eq = Eq()
neq = NEq()
lt = LT()
lte = LTE()
gt = GT()
gte = GTE()
