import json
import numpy as np

from field import FieldInt
from time import time
import field

import projective
import affine
import shared
from affine import AffinePoint
from field import FieldInt
from projective import ProjectivePoint

NUMBER_OF_TRIES = 1

def create_curve_params(raw_json):
    a, b, *_ = raw_json["invariants"]
    base_point = raw_json["basePoint"]
    field_order = raw_json["fieldOrder"]
    curve_order = raw_json["curveOrder"]
    curve_params = shared.CurveParams(
        base_point=shared.CurveBasePoint(*base_point),
        a=a,
        b=b,
        field_order=field_order,
        curve_order=curve_order,
    )
    affine.set_curve_params(curve_params)
    projective.set_curve_params(curve_params)
    field.set_modulus(field_order)
    return curve_params


def test_multiplication(basepoint):

    durations = []
    for _ in range(NUMBER_OF_TRIES):
        if isinstance(basepoint, ProjectivePoint):
            point = ProjectivePoint.random()
            scalar = ProjectivePoint.get_random_number()
        else:
            point = AffinePoint.random()
            scalar = AffinePoint.get_random_number()

        start = time()
        result = point * scalar
        durations.append(time() - start)

    durations = np.array(durations)
    return durations.mean(), durations.std()


def test_addition(basepoint):

    durations = []
    for _ in range(NUMBER_OF_TRIES):
        if isinstance(basepoint, ProjectivePoint):
            point = ProjectivePoint.random()
            scalar = ProjectivePoint.get_random_number()
        else:
            point = AffinePoint.random()
            scalar = AffinePoint.get_random_number()

        start = time()
        import pdb; pdb.set_trace()
        result = point + scalar.value
        durations.append(time() - start)

    durations = np.array(durations)
    return durations.mean(), durations.std()


def test_doubling(basepoint):

    durations = []
    for _ in range(NUMBER_OF_TRIES):
        if isinstance(basepoint, ProjectivePoint):
            point = ProjectivePoint.random()
        else:
            point = AffinePoint.random()
        start = time()
        result = point * FieldInt(2)
        durations.append(time() - start)

    durations = np.array(durations)
    return durations.mean(), durations.std()


if __name__ == "__main__":
    bit_lengths = [30, 70, 110, 150, 190]
    results = {}

    for representation in ["projective", "affine"]:
        results[representation] = {}

        for bit_length in bit_lengths:
            with open(f"params_{bit_length}.json", "r") as f:
                data = json.load(f)
            curve_params = create_curve_params(data)

            if representation == "projective":
                base_point = ProjectivePoint.get_base_point()
            else: 
                base_point = AffinePoint.get_base_point()

            avg_mul, std_mul = test_multiplication(base_point)
            # avg_add, std_add = test_addition(base_point)
            avg_double, std_double = test_doubling(base_point)

            results[representation][str(bit_length)] = {
                "avg_mul": avg_mul,
                "std_mul": std_mul,
                "avg_add": avg_add,
                "std_add": std_add,
                "avg_double": avg_double,
                "std_double": std_double,
            }
    import pdb

    pdb.set_trace()
    # # base_point = ProjectivePoint(172235452673, 488838007757, 1)
    # # # start = time()
    # # # duration = time() - start/
