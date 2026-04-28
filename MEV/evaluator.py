from __future__ import annotations
from MEV.nodes.base import Expr, Value
from MEV.registry import Registry, default_registry


def compute(
    expr: Expr,
    ctx: dict,
    registry: Registry | None = None,
    target_unit: str | None = None,
) -> Value:
    reg = registry or default_registry()
    result = expr.eval(ctx, reg)
    if target_unit is not None:
        from MEV.units.pint_adapter import eval_quantity, quantity_to_value
        return quantity_to_value(eval_quantity(result), target_unit)
    return result
