import dataclasses
import random

import affine
import pollard_rho_base


@dataclasses.dataclass
class EcAffinePollardRhoDLParams:
    base_point: affine.AffinePoint
    mul_point: affine.AffinePoint
    field_order: int
    curve_order: int

    def __str__(self):
        return (
            f"EcAffinePollardRhoDLParams"
            f"(base_point={self.base_point}, q_point={self.q_point})"
        )


@dataclasses.dataclass
class Coeffs:
    alpha: int = 0
    beta: int = 0


def generate_params(
    curve_params: affine.CurveParams, value_to_find: int = None
) -> EcAffinePollardRhoDLParams:
    base_point = affine.AffinePoint(
        curve_params.base_point.x, curve_params.base_point.y
    )
    value_to_find = value_to_find or random.randint(2, curve_params.curve_order)
    mul_result = value_to_find * base_point
    return EcAffinePollardRhoDLParams(
        base_point=base_point,
        mul_point=mul_result,
        field_order=curve_params.field_order,
        curve_order=curve_params.curve_order,
    )


class EcAffinePollardRhoDL(pollard_rho_base.AbstractEcPollardRhoDL):
    def __init__(self, params: EcAffinePollardRhoDLParams):
        self.base_point: affine.AffinePoint = params.base_point
        self.mul_point: affine.AffinePoint = params.mul_point
        self.field_order: int = params.field_order
        self.curve_order: int = params.curve_order

