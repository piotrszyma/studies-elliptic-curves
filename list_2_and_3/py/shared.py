import dataclasses


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
