# MEV — Math Expression Validator

A small symbolic expression framework that builds expression ASTs, validates
them against runtime data, and only evaluates after validation succeeds. This
prevents partial side effects from runtime errors like division-by-zero or wrong unit.

Expressions are **unit-aware** via [Pint](https://pint.readthedocs.io): every
variable and literal can carry a physical unit (`"km"`, `"s"`, `"kg"`, etc.).
During validation, MEV tracks dimensional analysis through the whole expression
tree. It catches unit mismatches (e.g. adding metres to seconds) and can
assert that the result lands in an expected unit (e.g. `"km/s"`). Context
values can be plain scalars (interpreted in the variable's declared unit) or
`(value, unit)` tuples to supply a different unit at runtime, with automatic
conversion applied before evaluation.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Building expressions

**Builder API** - compose expressions from Python:

```python
from MEV import var, val, sqrt

expr = (val(120.0) - val(10.0)) / var("quantity")
expr_with_units = val(120.0, "km") / var("time", "s")
hypotenuse = sqrt(var("a") ** 2 + var("b") ** 2)
```

## Validation and evaluation

```python
from MEV import var, val
from MEV.validator import validateFull

expr = (val(120.0) - val(10.0)) / var("quantity")

ok, message = expr.validate({"quantity": 2})
if ok:
    print(expr.evaluate({"quantity": 2}).value)  # 55.0

errors = validateFull(expr, {"quantity": 0})
for e in errors:
    print(e)
```

Use `target_unit=` on either call to also validate dimensional correctness:

```python
ok, msg = expr.validate(ctx, target_unit="km/s")
errors  = validateFull(expr, ctx, target_unit="km/s")
```

Context values can be raw scalars (interpreted in the variable's declared unit)
or `(value, unit)` tuples for an explicit unit override.

## Available math functions

| Function | Notes |
|---|---|
| `sqrt(x)` | square root |
| `exp(x)` | e^x |
| `log(x)`, `log(x, base)` | log₁₀ or arbitrary base |
| `ln(x)` | natural log |
| `abs_fn(x)` | absolute value |
| `round_fn(x)`, `round_fn(x, dp)` | round to dp decimal places |
| `ceil(x)`, `floor(x)` | ceiling / floor |
| `sin(x)`, `cos(x)`, `tan(x)` | trig (radians) |
| `asin(x)`, `acos(x)`, `atan(x)`, `atan2(y, x)` | inverse trig |
| `fn(name, *args)` | call any registered custom function |

## Examples

```bash
python real_life_example/lab_calculation/lab_calculation.py
python real_life_example/messy_data/messy_data_handling.py
```

