from __future__ import annotations
from dataclasses import dataclass

# The error object have message and kind of error
@dataclass(frozen=True)
class ValidationError:
    kind: str
    message: str
    line: int | None = None
    col: int | None = None

    def __str__(self) -> str:
        loc = f" (line {self.line}, col {self.col})" if self.line is not None else ""
        return f"[{self.kind}] {self.message}{loc}"

# This is what evaluate return (value:...,unit:....)
@dataclass(frozen=True)
class Value:
    value: object
    unit: str | None = None

    def __repr__(self) -> str:
        if self.unit:
            return f"Value({self.value!r}, unit={self.unit!r})"
        return f"Value({self.value!r})"

# Turn the expression in to an AST
def promote(x: object) -> "Expr":
    if isinstance(x, Expr):
        return x
    from MEV.nodes.literals import NumberLiteral
    from MEV.nodes.variables import Variable
    if isinstance(x, bool):
        raise TypeError("Boolean values are not supported")
    if isinstance(x, (int, float)):
        return NumberLiteral(x)
    if isinstance(x, str):
        return Variable(x)
    raise TypeError(f"Cannot use {type(x).__name__!r} in an expression; just use string or number")

# Node base class
class Expr:

    line: int | None = None
    col: int | None = None

    def validate(
        self,
        ctx: dict,
        target_unit: str | None = None,
    ) -> tuple[bool, str | None]:
        
        from MEV.validator import validateFull
        errors = validateFull(self, ctx, target_unit)
        if not errors:
            return (True, None)
        return (False, errors[0].message)

    def evaluate(self, ctx: dict, target_unit: str | None = None, *, registry=None) -> Value:
        from MEV.evaluator import compute
        return compute(self, ctx, registry, target_unit)

    # To check error for each node
    def errors(self, ctx: dict) -> list[ValidationError]:
        raise NotImplementedError

    # To return value for each node
    def eval(self, ctx: dict, registry) -> Value:
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError



    # Arithmetic operators 
    #__operator__ will handle the situation where expresion like var(5) on the left
    #__roperator__ will handle the situation when it on the right
    def __add__(self, other):
        from MEV.nodes.operators import Add
        return Add(self, promote(other))

    def __radd__(self, other):
        from MEV.nodes.operators import Add
        return Add(promote(other), self)

    def __sub__(self, other):
        from MEV.nodes.operators import Sub
        return Sub(self, promote(other))

    def __rsub__(self, other):
        from MEV.nodes.operators import Sub
        return Sub(promote(other), self)

    def __mul__(self, other):
        from MEV.nodes.operators import Mul
        return Mul(self, promote(other))

    def __rmul__(self, other):
        from MEV.nodes.operators import Mul
        return Mul(promote(other), self)

    def __truediv__(self, other):
        from MEV.nodes.operators import Div
        return Div(self, promote(other))

    def __rtruediv__(self, other):
        from MEV.nodes.operators import Div
        return Div(promote(other), self)

    def __pow__(self, other):
        from MEV.nodes.operators import Pow
        return Pow(self, promote(other))

    def __rpow__(self, other):
        from MEV.nodes.operators import Pow
        return Pow(promote(other), self)

    def __neg__(self):
        from MEV.nodes.operators import UnaryMinus
        return UnaryMinus(self)
