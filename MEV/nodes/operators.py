from __future__ import annotations
from dataclasses import dataclass
from .base import Expr, ValidationError, Value

# This will handle the logic for arithmetic operation
@dataclass(frozen=True)
class BinaryOp(Expr):
    left: Expr
    right: Expr
    line: int | None = None
    col: int | None = None

    def opName(self) -> str:
        return type(self).__name__

    def errors(self, ctx: dict) -> list[ValidationError]:
        return list(self.left.errors(ctx)) + list(self.right.errors(ctx))

    def evalBinary(self, left_q, right_q):
        raise NotImplementedError

    def eval(self, ctx: dict, registry) -> Value:
        from MEV.units.pint_adapter import eval_quantity, quantity_to_value
        lq = eval_quantity(self.left.eval(ctx, registry))
        rq = eval_quantity(self.right.eval(ctx, registry))
        return quantity_to_value(self.evalBinary(lq, rq), None)

    def to_dict(self) -> dict:
        return {
            "type": self.opName(),
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }


@dataclass(frozen=True)
class Add(BinaryOp):
    def evalBinary(self, l, r): return l + r


@dataclass(frozen=True)
class Sub(BinaryOp):
    def evalBinary(self, l, r): return l - r


@dataclass(frozen=True)
class Mul(BinaryOp):
    def evalBinary(self, l, r): return l * r


@dataclass(frozen=True)
class Div(BinaryOp):
    def errors(self, ctx: dict) -> list[ValidationError]:
        errors = super().errors(ctx)
        from MEV.nodes.literals import NumberLiteral
        from MEV.nodes.variables import Variable
        if isinstance(self.right, NumberLiteral) and self.right.value == 0:
            errors.append(ValidationError(
                kind="DivisionByZero",
                message="literal denominator is 0 — division by zero",
                line=self.right.line, col=self.right.col,
            ))
        elif isinstance(self.right, Variable) and self.right.name in ctx:
            raw = ctx[self.right.name]
            v = raw[0] if isinstance(raw, tuple) else raw
            if v == 0:
                errors.append(ValidationError(
                    kind="DivisionByZero",
                    message=f"'{self.right.name}' is 0 — division by zero",
                    line=self.right.line, col=self.right.col,
                ))
        return errors

    def evalBinary(self, l, r): return l / r


@dataclass(frozen=True)
class Pow(BinaryOp):
    def evalBinary(self, l, r): return l ** r


@dataclass(frozen=True)
class UnaryMinus(Expr):
    operand: Expr
    line: int | None = None
    col: int | None = None

    def errors(self, ctx: dict) -> list[ValidationError]:
        return list(self.operand.errors(ctx))

    def eval(self, ctx: dict, registry) -> Value:
        from MEV.units.pint_adapter import eval_quantity, quantity_to_value
        return quantity_to_value(-eval_quantity(self.operand.eval(ctx, registry)), None)

    def to_dict(self) -> dict:
        return {"type": "UnaryMinus", "operand": self.operand.to_dict()}
