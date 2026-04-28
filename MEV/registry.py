
from __future__ import annotations
import math
import pint
from MEV.units.pint_adapter import get_registry

#Just to map function like sqrt to data
class Registry(dict):
    def register(self, name: str, arity: int | None = None, unit_rule: str | None = None):
        def decorator(fn):
            self[name] = {"fn": fn, "arity": arity, "unit_rule": unit_rule}
            return fn
        return decorator

#Extract magnitude from a Quantity or plain number.
def magnitude(q) -> float:
    if isinstance(q, pint.Quantity):
        return float(q.magnitude)
    return float(q)

#wraps a plain float back into a pint quantity
def quantity(value: float, unit=None):
    ureg = get_registry()
    if unit is None:
        return ureg.Quantity(value)
    return ureg.Quantity(value, unit)

#standard math function
def buildDefault() -> Registry:
    reg = Registry()

    @reg.register("sqrt", arity=1)
    def sqrt(x):
        return quantity(math.sqrt(magnitude(x)), getattr(x, "units", None))

    @reg.register("log", arity=None)
    def log(x, base=None):
        if base is None:
            return quantity(math.log(magnitude(x)))
        return quantity(math.log(magnitude(x), magnitude(base)))

    @reg.register("ln", arity=1)
    def ln(x):
        return quantity(math.log(magnitude(x)))

    @reg.register("abs", arity=1)
    def abs_(x):
        ureg = get_registry()
        if isinstance(x, pint.Quantity):
            return abs(x)
        return quantity(abs(magnitude(x)))

    @reg.register("round", arity=None) 
    def round_(x, dp=None):
        dp_int = int(magnitude(dp)) if dp is not None else 0
        if isinstance(x, pint.Quantity):
            return quantity(round(float(x.magnitude), dp_int), x.units)
        return quantity(round(magnitude(x), dp_int))

    @reg.register("sin", arity=1)
    def sin(x):
        ureg = get_registry()
        if isinstance(x, pint.Quantity) and x.dimensionality == ureg.radian.dimensionality:
            return quantity(math.sin(x.to("radian").magnitude))
        return quantity(math.sin(magnitude(x)))

    @reg.register("cos", arity=1)
    def cos(x):
        ureg = get_registry()
        if isinstance(x, pint.Quantity) and x.dimensionality == ureg.radian.dimensionality:
            return quantity(math.cos(x.to("radian").magnitude))
        return quantity(math.cos(magnitude(x)))

    @reg.register("tan", arity=1)
    def tan(x):
        ureg = get_registry()
        if isinstance(x, pint.Quantity) and x.dimensionality == ureg.radian.dimensionality:
            return quantity(math.tan(x.to("radian").magnitude))
        return quantity(math.tan(magnitude(x)))

    @reg.register("asin", arity=1)
    def asin(x):
        return quantity(math.asin(magnitude(x)))

    @reg.register("acos", arity=1)
    def acos(x):
        return quantity(math.acos(magnitude(x)))

    @reg.register("atan", arity=1)
    def atan(x):
        return quantity(math.atan(magnitude(x)))

    @reg.register("atan2", arity=2)
    def atan2(y, x):
        return quantity(math.atan2(magnitude(y), magnitude(x)))

    @reg.register("exp", arity=1)
    def exp(x):
        return quantity(math.exp(magnitude(x)))

    @reg.register("ceil", arity=1)
    def ceil(x):
        if isinstance(x, pint.Quantity):
            return quantity(math.ceil(x.magnitude), x.units)
        return quantity(math.ceil(magnitude(x)))

    @reg.register("floor", arity=1)
    def floor(x):
        if isinstance(x, pint.Quantity):
            return quantity(math.floor(x.magnitude), x.units)
        return quantity(math.floor(magnitude(x)))

    return reg


_defaultReg: Registry | None = None

#builds the default registry once on first call and reuses it.
def default_registry() -> Registry:
    global _defaultReg
    if _defaultReg is None:
        _defaultReg = buildDefault()
    return _defaultReg
