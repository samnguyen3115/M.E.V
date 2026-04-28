#!/usr/bin/env python3
"""Messy velocity analysis demo for MEV."""

from __future__ import annotations

import csv
from functools import reduce
from pathlib import Path
from typing import Iterable

from MEV import val


CSV_PATH = Path(__file__).with_name("messy_velocity_data.csv")

# Average the raw numbers without fixing the units first
def average_speed_naive(rows: Iterable[dict[str, str]]) -> float:
    
    speeds = [float(row["speed"]) for row in rows]
    return sum(speeds) / len(speeds)

#Average after manually normalizing every row with if/else logic
def average_speed_if_else(rows: Iterable[dict[str, str]], target_unit: str = "m/s") -> float:
    total = 0.0
    count = 0

    for row in rows:
        speed = float(row["speed"])
        unit = row["unit"]

        if unit == "m/s":
            speed_mps = speed
        elif unit == "km/h":
            speed_mps = speed / 3.6
        elif unit == "mph":
            speed_mps = speed * 0.44704
        else:
            raise ValueError(f"Unsupported speed unit: {unit}")

        if target_unit == "m/s":
            normalized = speed_mps
        elif target_unit == "km/h":
            normalized = speed_mps * 3.6
        elif target_unit == "mph":
            normalized = speed_mps / 0.44704
        else:
            raise ValueError(f"Unsupported target unit: {target_unit}")

        total += normalized
        count += 1

    return total / count

#Average with MEV
def average_speed_with_library(rows: Iterable[dict[str, str]], target_unit: str = "m/s") -> float:
    expressions = [val(float(row["speed"]), row["unit"]) for row in rows]
    expr = reduce(lambda left, right: left + right, expressions) / len(expressions)

    ok, message = expr.validate({}, target_unit=target_unit)
    if not ok:
        raise ValueError(message)

    return float(expr.evaluate({}, target_unit=target_unit).value)


def main() -> None:
    with CSV_PATH.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    naive = average_speed_naive(rows)
    manual_mps = average_speed_if_else(rows, target_unit="m/s")
    library_mps = average_speed_with_library(rows, target_unit="m/s")

    print(f"Naive average: {naive:.2f}")
    print(f"Manual average in m/s: {manual_mps:.2f}")
    print(f"Library average in m/s: {library_mps:.2f}")


if __name__ == "__main__":
    main()