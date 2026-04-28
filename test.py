#!/usr/bin/env python3
"""Test file to demonstrate MEV library usage."""

from MEV import (
    var, val, sqrt
)

def test():
    expr = sqrt(var("x","meters/second")-val(10,"meters"))

    print(expr.validate({"x":10},target_unit="meters/second"))

if __name__ == "__main__":
    test()




    