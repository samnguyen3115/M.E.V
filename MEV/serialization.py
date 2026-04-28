from __future__ import annotations
from MEV.nodes.base import Expr

_nodeMapCache: dict[str, type] | None = None


def nodeMap() -> dict[str, type]:
    global _nodeMapCache
    if _nodeMapCache is not None:
        return _nodeMapCache
    from MEV.nodes.literals import NumberLiteral
    from MEV.nodes.variables import Variable
    from MEV.nodes.operators import (
        Add, Sub, Mul, Div, Pow, UnaryMinus,
    )
    from MEV.nodes.functions import MathOp

    _nodeMapCache = {
        "NumberLiteral": NumberLiteral,
        "Variable": Variable,
        "Add": Add, "Sub": Sub, "Mul": Mul, "Div": Div,
        "Pow": Pow,
        "UnaryMinus": UnaryMinus,
        "MathOp": MathOp,
    }
    return _nodeMapCache


def deserialize(d: dict) -> Expr:
    node_type = d["type"]
    cls = nodeMap().get(node_type)
    if cls is None:
        raise ValueError(f"Unknown node type: {node_type!r}")

    from MEV.nodes.literals import NumberLiteral
    from MEV.nodes.variables import Variable
    from MEV.nodes.operators import UnaryMinus
    from MEV.nodes.functions import MathOp

    if node_type == "NumberLiteral":
        return NumberLiteral(d["value"], d.get("unit"))
    if node_type == "Variable":
        return Variable(d["name"], d.get("unit"))
    if node_type == "UnaryMinus":
        return UnaryMinus(deserialize(d["operand"]))
    if node_type == "MathOp":
        return MathOp(d["name"], tuple(deserialize(a) for a in d["args"]))
    # Binary nodes: all have left + right
    return cls(deserialize(d["left"]), deserialize(d["right"]))
