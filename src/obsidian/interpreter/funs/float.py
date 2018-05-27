from ..types import PrimFun, Panic, Int, Float, Symbol, true, false


class Add(PrimFun):
    def __init__(self):
        super().__init__('add', ['a', 'b'])
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
        super().__init__('sub', ['a', 'b'])
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
        super().__init__('mul', ['a', 'b'])
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
        super().__init__('div', ['a', 'b'])
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
        super().__init__('floor_div', ['a', 'b'])
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
        super().__init__('mod', ['a', 'b'])
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
        super().__init__('pow', ['a', 'b'])
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
        super().__init__('eq', variadic=True)
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
        super().__init__('eq', variadic=True)
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


add = Add()
sub = Sub()
mul = Mul()
div = Div()
floor_div = FloorDiv()
mod = Mod()
pow = Pow()
eq = Eq()
neq = NEq()
