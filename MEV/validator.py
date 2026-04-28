from __future__ import annotations
from MEV.nodes.base import Expr, ValidationError
from MEV.units.pint_adapter import check_unit_compatibility


def validateFull(expr: Expr, ctx: dict, target_unit: str | None = None) -> list[ValidationError]:
    errors: list[ValidationError] = []
    errors.extend(checkContextTypes(ctx))
    errors.extend(expr.errors(ctx))
    if not errors:
        errors.extend(checkEvaluation(expr, ctx))
    if target_unit and not errors:
        errors.extend(checkTargetUnit(expr, ctx, target_unit))
    return errors


def checkContextTypes(ctx: dict) -> list[ValidationError]:
    errors = []
    for key, val in ctx.items():
        if val is None:
            continue
        raw = val[0] if isinstance(val, tuple) else val
        if not isinstance(raw, (int, float, bool, str)):
            errors.append(ValidationError(
                kind="TypeError",
                message=f"'{key}' has unsupported type {type(raw).__name__}",
            ))
    return errors


def checkTargetUnit(expr: Expr, ctx: dict, target_unit: str) -> list[ValidationError]:
    from MEV.units.pint_adapter import eval_quantity
    try:
        result = expr.eval(ctx, None)
        rq = eval_quantity(result)
        msg = check_unit_compatibility(rq, target_unit)
        if msg:
            return [ValidationError(kind="UnitConversionError", message=msg)]
    except Exception:
        pass
    return []


def checkEvaluation(expr: Expr, ctx: dict) -> list[ValidationError]:
    try:
        expr.eval(ctx, None)
    except Exception as e:
        return [ValidationError(kind="EvaluationError", message=str(e))]
    return []
