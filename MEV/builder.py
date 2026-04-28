from __future__ import annotations
from MEV.nodes.base import promote, Expr
from MEV.nodes.literals import NumberLiteral
from MEV.nodes.variables import Variable
from MEV.nodes.functions import MathOp


#Function to declare a variable
def var(name: str, unit: str | None = None) -> Variable:
    """Declare one symbolic variable with an optional expected unit."""
    return Variable(name, unit=unit)


#Function to declare a constant value
def val(value, unit: str | None = None) -> NumberLiteral:
    if isinstance(value, bool):
        raise TypeError("val() only accepts numeric values, got bool")
    if isinstance(value, (int, float)):
        return NumberLiteral(value, unit)
    raise TypeError(f"Cannot create constant from {type(value).__name__}")


#All the supported math function
def sqrt(x) -> MathOp:
    return MathOp("sqrt", (promote(x),))

def log(x, base=None) -> MathOp:
    if base is None:
        return MathOp("log", (promote(x),))
    return MathOp("log", (promote(x), promote(base)))

def ln(x) -> MathOp:
    return MathOp("ln", (promote(x),))

def abs_fn(x) -> MathOp:
    return MathOp("abs", (promote(x),))

def round_fn(x, dp=None) -> MathOp:
    if dp is None:
        return MathOp("round", (promote(x),))
    return MathOp("round", (promote(x), promote(dp)))

def sin(x) -> MathOp:
    return MathOp("sin", (promote(x),))

def cos(x) -> MathOp:
    return MathOp("cos", (promote(x),))

def tan(x) -> MathOp:
    return MathOp("tan", (promote(x),))

def asin(x) -> MathOp:
    return MathOp("asin", (promote(x),))

def acos(x) -> MathOp:
    return MathOp("acos", (promote(x),))

def atan(x) -> MathOp:
    return MathOp("atan", (promote(x),))

def atan2(y, x) -> MathOp:
    return MathOp("atan2", (promote(y), promote(x)))

def exp(x) -> MathOp:
    return MathOp("exp", (promote(x),))

def ceil(x) -> MathOp:
    return MathOp("ceil", (promote(x),))

def floor(x) -> MathOp:
    return MathOp("floor", (promote(x),))


# Custom math function
def fn(name: str, *args) -> MathOp:
    return MathOp(name, tuple(promote(a) for a in args))

