from __future__ import annotations
from dataclasses import dataclass
from .base import Expr, ValidationError, Value

#THis class will handle a variable  with unit and put it in the tree
@dataclass(frozen=True)
class Variable(Expr):
    name: str
    unit: str | None = None
    line: int | None = None
    col: int | None = None

    def errors(self, ctx: dict) -> list[ValidationError]:
        if self.name not in ctx:
            return [ValidationError(
                kind="UndefinedVariable",
                message=f"'{self.name}' is not defined in context",
                line=self.line, col=self.col,
            )]
        if ctx[self.name] is None:
            return [ValidationError(
                kind="NullError",
                message=f"'{self.name}' is None",
                line=self.line, col=self.col,
            )]
        return []

    def eval(self, ctx: dict, registry) -> Value:
        from MEV.units.pint_adapter import make_quantity, quantity_to_value
        import pint

        raw = ctx[self.name]
        if isinstance(raw, tuple):
            val, input_unit = raw
            q = make_quantity(val, input_unit)
        else:
            # If variable has a declared unit, plain scalars are interpreted in that unit.
            q = make_quantity(raw, self.unit)

        # Enforce declared variable unit by converting all inputs to it.
        if self.unit is not None:
            try:
                q = q.to(self.unit)
            except (pint.DimensionalityError, pint.UndefinedUnitError):
                # Let validate() report this via EvaluationError path.
                raise
        return quantity_to_value(q, None)

    def to_dict(self) -> dict:
        d: dict = {"type": "Variable", "name": self.name}
        if self.unit is not None:
            d["unit"] = self.unit
        return d
