from __future__ import annotations

from MEV import val

#Divide the raw values without checking whether the units make sense.
def calculate_speed_naive(distance_km: float, time_s: float) -> float:
    return distance_km / time_s

#Calculate speed with MEV and validate the target unit first.
def validate_speed_with_library(
    distance_km: float,
    time_s: float,
    target_unit: str = "km",
) -> tuple[bool, str | None]:
    expr = val(distance_km, "km") / val(time_s, "s")

    return expr.validate({}, target_unit=target_unit)


def main() -> None:
    distance_km = 120.0
    time_s = 30.0

    naive_speed = calculate_speed_naive(distance_km, time_s)
    library_result = validate_speed_with_library(distance_km, time_s, target_unit="km")

    print(f"Naive speed: {naive_speed:.2f} km")
    print(f"Library Result: {library_result}")


if __name__ == "__main__":
    main()