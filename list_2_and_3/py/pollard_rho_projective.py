import dataclasses
import random

import projective
import pollard_rho_base


@dataclasses.dataclass
class EcProjectivePollardRhoDLParams:
    base_point: projective.ProjectivePoint
    mul_point: projective.ProjectivePoint
    field_order: int
    curve_order: int

    def __str__(self):
        return (
            f"EcProjectivePollardRhoDLParams"
            f"(base_point={self.base_point}, q_point={self.q_point})"
        )


def generate_params(
    curve_params: projective.CurveParams,
) -> EcProjectivePollardRhoDLParams:
    base_point = projective.ProjectivePoint(
        curve_params.base_point.x, curve_params.base_point.y, curve_params.base_point.z
    )

    k = random.randint(2, curve_params.curve_order)
    mul_result = k * base_point
    return EcProjectivePollardRhoDLParams(
        base_point=base_point,
        mul_point=mul_result,
        field_order=curve_params.field_order,
        curve_order=curve_params.curve_order,
    )


class EcProjectivePollardRhoDL(pollard_rho_base.AbstractEcPollardRhoDL):
    def __init__(self, params: EcProjectivePollardRhoDLParams):
        self.base_point: projective.ProjectivePoint = params.base_point
        self.mul_point: projective.ProjectivePoint = params.mul_point
        self.field_order: int = params.field_order
        self.curve_order: int = params.curve_order
