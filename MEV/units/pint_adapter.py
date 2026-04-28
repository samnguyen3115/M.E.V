
from __future__ import annotations
import pint
from MEV.nodes.base import Value

_ureg: pint.UnitRegistry | None = None


def get_registry() -> pint.UnitRegistry:
    global _ureg
    if _ureg is None:
        _ureg = pint.UnitRegistry()
    return _ureg

#Wrap a plain Python number in a pint quantity#
def make_quantity(value, unit: str | None):
    ureg = get_registry()
    if unit is None:
        return ureg.Quantity(value)
    return ureg.Quantity(value, unit)

#Convert a value back to a pint quantity
def eval_quantity(v: Value):
    ureg = get_registry()
    if isinstance(v, pint.Quantity):
        return v
    if isinstance(v, Value):
        raw = v.value
        if not isinstance(raw, (int, float)) or isinstance(raw, bool):
            return raw
        if v.unit is None:
            return ureg.Quantity(raw)
        return ureg.Quantity(raw, v.unit)
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        return v
    return ureg.Quantity(v)

#Convert a pint quantity to an MEV Value
def quantity_to_value(q, target_unit: str | None) -> Value:
    ureg = get_registry()

    if not isinstance(q, pint.Quantity):
        return Value(q)

    if target_unit is not None:
        q = q.to(target_unit)

    if q.dimensionless:
        mag = float(q.to_base_units().magnitude)
        return Value(mag)

    unit_str = target_unit if target_unit is not None else f"{q.units:~P}"
    return Value(float(q.magnitude), unit_str)


def quantity_magnitude(raw) -> float | int:
    if isinstance(raw, tuple):
        return raw[0]
    return raw


def check_unit_compatibility(result_q, target_unit: str) -> str | None:
    ureg = get_registry()
    try:
        result_q.to(target_unit)
        return None
    except pint.DimensionalityError as e:
        result_dim = str(result_q.dimensionality)
        return f"Result is {result_dim} but target unit '{target_unit}' is incompatible: {e}"
    except pint.UndefinedUnitError as e:
        return f"Unknown target unit '{target_unit}': {e}"
