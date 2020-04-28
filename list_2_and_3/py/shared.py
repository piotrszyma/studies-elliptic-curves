import dataclasses


def modinv(value: int, modulus: int) -> int:
    inverse, tmp = 1, 0
    while modulus:
        quotient, reminder = divmod(value, modulus)
        value, inverse, tmp, modulus = modulus, tmp, inverse - quotient * tmp, reminder
    if value == 1:
        return inverse
    raise ValueError(f"{value} is not invertible modulo {modulus}")


@dataclasses.dataclass
class CurveBasePoint:
    x: int
    y: int
    z: int = 1


@dataclasses.dataclass
class CurveParams:
    base_point: CurveBasePoint
    a: int
    b: int
    curve_order: int
    field_order: int
