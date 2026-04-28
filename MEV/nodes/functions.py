from __future__ import annotations
from dataclasses import dataclass
from .base import Expr, ValidationError, Value

#This will handle any math function call like sqrt or log
@dataclass(frozen=True)
class MathOp(Expr):
    name: str
    args: tuple[Expr, ...]
    line: int | None = None
    col: int | None = None

    def errors(self, ctx: dict) -> list[ValidationError]:
        from MEV.registry import default_registry
        errors: list[ValidationError] = []

        for arg in self.args:
            errors.extend(arg.errors(ctx))

        reg = default_registry()
        if self.name not in reg:
            errors.append(ValidationError(
                kind="UnknownFunction",
                message=f"Function '{self.name}' is not registered",
                line=self.line, col=self.col,
            ))
            return errors

        fn_meta = reg[self.name]
        arity = fn_meta.get("arity")
        if arity is not None and len(self.args) != arity:
            errors.append(ValidationError(
                kind="ArityError",
                message=f"'{self.name}' expects {arity} argument(s), got {len(self.args)}",
                line=self.line, col=self.col,
            ))

        if not errors and self.name == "sqrt":
            from MEV.nodes.literals import NumberLiteral
            from MEV.nodes.variables import Variable
            arg = self.args[0]
            if isinstance(arg, NumberLiteral) and arg.value < 0:
                errors.append(ValidationError(
                    kind="DomainError",
                    message=f"sqrt argument is negative ({arg.value})",
                    line=arg.line, col=arg.col,
                ))
            elif isinstance(arg, Variable) and arg.name in ctx:
                raw = ctx[arg.name]
                v = raw[0] if isinstance(raw, tuple) else raw
                if isinstance(v, (int, float)) and v < 0:
                    errors.append(ValidationError(
                        kind="DomainError",
                        message=f"sqrt argument is negative ({v})",
                        line=arg.line, col=arg.col,
                    ))

        if not errors and self.name in ("log", "ln"):
            from MEV.nodes.literals import NumberLiteral
            from MEV.nodes.variables import Variable
            arg = self.args[0]
            if isinstance(arg, NumberLiteral) and arg.value <= 0:
                errors.append(ValidationError(
                    kind="DomainError",
                    message=f"log argument must be positive (got {arg.value})",
                    line=arg.line, col=arg.col,
                ))
            elif isinstance(arg, Variable) and arg.name in ctx:
                raw = ctx[arg.name]
                v = raw[0] if isinstance(raw, tuple) else raw
                if isinstance(v, (int, float)) and v <= 0:
                    errors.append(ValidationError(
                        kind="DomainError",
                        message=f"log argument must be positive (got {v})",
                        line=arg.line, col=arg.col,
                    ))

        return errors

    def eval(self, ctx: dict, registry) -> Value:
        from MEV.registry import default_registry
        from MEV.units.pint_adapter import eval_quantity, quantity_to_value

        reg = registry or default_registry()
        fn_meta = reg[self.name]
        fn = fn_meta["fn"]
        qty_args = [eval_quantity(a.eval(ctx, registry)) for a in self.args]
        return quantity_to_value(fn(*qty_args), None)

    def to_dict(self) -> dict:
        return {
            "type": "MathOp",
            "name": self.name,
            "args": [a.to_dict() for a in self.args],
        }
