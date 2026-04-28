from __future__ import annotations
from dataclasses import dataclass
from .base import Expr, ValidationError, Value

#THis class will handle a constant value with unit and put it in the tree
@dataclass(frozen=True)
class NumberLiteral(Expr):
    value: float | int
    unit: str | None = None
    line: int | None = None
    col: int | None = None

    def errors(self, ctx: dict) -> list[ValidationError]:
        return []

    def eval(self, ctx: dict, registry) -> Value:
        from MEV.units.pint_adapter import make_quantity, quantity_to_value
        return quantity_to_value(make_quantity(self.value, self.unit), None)

    def to_dict(self) -> dict:
        d: dict = {"type": "NumberLiteral", "value": self.value}
        if self.unit:
            d["unit"] = self.unit
        return d
