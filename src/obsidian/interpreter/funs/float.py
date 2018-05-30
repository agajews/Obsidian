from ..types import (
    PrimFun,
    Int,
    Float,
    Symbol,
    Map,
    String,
    true,
    false,
)
from ..types.ast import ASTString, ASTFloat
from .get_attr import get_attr


class FloatConstructor(PrimFun):
    def __init__(self):
        super().__init__('Float', ['ast'])

    def macro(self, scope, ast):
        self.typecheck_arg(ast, ASTFloat)
        ast.validate()
        float = Float(ast.get('float').float)
        sigil = ast.get('sigil')
        if sigil.str == '':
            return float
        constructors = Float.T.get('sigils')
        constructor = get_attr.fun(
            constructors, String('get')).call(scope, [ASTString(sigil)])
        return constructor.call(scope, [ASTFloat(float)])


class FloatToStr(PrimFun):
    def __init__(self):
        super().__init__('Float.to_str', ['float'])

    def fun(self, float):
        self.typecheck_arg(float, Float)
        return String(str(float.float))


class FloatEq(PrimFun):
    def __init__(self):
        super().__init__('Float.eq', ['a', 'b'])

    def fun(self, a, b):
        self.typecheck_arg(a, Float)
        self.typecheck_arg(b, Float)
        return true if a.float == b.float else false


class FloatHash(PrimFun):
    def __init__(self):
        super().__init__('Float.hash', ['float'])

    def fun(self, float):
        self.typecheck_arg(float, Float)
        return Int(hash(float.float))


class Add(PrimFun):
    def __init__(self):
        super().__init__('float.add', ['a', 'b'])
        self.set('precedence', Int(6))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        self.typecheck_arg(a, Float)
        self.typecheck_arg(b, Float)
        return Float(a.float + b.float)


class Sub(PrimFun):
    def __init__(self):
        super().__init__('float.sub', ['a', 'b'])
        self.set('precedence', Int(6))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        self.typecheck_arg(a, Float)
        self.typecheck_arg(b, Float)
        return Float(a.float - b.float)


class Mul(PrimFun):
    def __init__(self):
        super().__init__('float.mul', ['a', 'b'])
        self.set('precedence', Int(7))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        self.typecheck_arg(a, Float)
        self.typecheck_arg(b, Float)
        return Float(a.float * b.float)


class Div(PrimFun):
    def __init__(self):
        super().__init__('float.div', ['a', 'b'])
        self.set('precedence', Int(7))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        self.typecheck_arg(a, Float)
        self.typecheck_arg(b, Float)
        return Float(a.float / b.float)


class FloorDiv(PrimFun):
    def __init__(self):
        super().__init__('float.floor_div', ['a', 'b'])
        self.set('precedence', Int(7))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        self.typecheck_arg(a, Float)
        self.typecheck_arg(b, Float)
        return Float(a.float // b.float)


class Mod(PrimFun):
    def __init__(self):
        super().__init__('float.mod', ['a', 'b'])
        self.set('precedence', Int(7))
        self.set('associativity', Symbol('left'))

    def fun(self, a, b):
        self.typecheck_arg(a, Float)
        self.typecheck_arg(b, Float)
        return Float(a.float % b.float)


class Pow(PrimFun):
    def __init__(self):
        super().__init__('float.pow', ['a', 'b'])
        self.set('precedence', Int(8))
        self.set('associativity', Symbol('right'))

    def fun(self, a, b):
        self.typecheck_arg(a, Float)
        self.typecheck_arg(b, Float)
        return Float(a.float ** b.float)


class Eq(PrimFun):
    def __init__(self):
        super().__init__('float.eq', variadic=True)
        self.set('precedence', Int(4))
        self.set('associativity', Symbol('none'))

    def fun(self, *nums):
        for i, num in enumerate(nums):
            self.typecheck_arg(num, Float)
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
            self.typecheck_arg(num, Float)
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
            self.typecheck_arg(num, Float)
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
            self.typecheck_arg(num, Float)
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
            self.typecheck_arg(num, Float)
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
            self.typecheck_arg(num, Float)
        for a, b in zip(nums[:-1], nums[1:]):
            if a.float < b.float:
                return false
        return true


Float.T.set('call', FloatConstructor())
Float.T.get('methods').set('to_str', FloatToStr())
Float.T.get('methods').set('eq', FloatEq())
Float.T.get('methods').set('hash', FloatHash())
Float.T.set('sigils', Map({}))
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
