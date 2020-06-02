import argparse
import random
from field import FieldInt
import projective
import copy
import setup

ProjectivePoint = projective.ProjectivePoint


def main(args):
    curve_params, bit_length = setup.set_curve_params(args)
    print(curve_params)
    k = args.k if args.k is not None else random.getrandbits(bit_length)
    base_point = ProjectivePoint(
        x=curve_params.base_point.x,
        y=curve_params.base_point.y,
        z=curve_params.base_point.z,
    )
    mul_point = base_point * k
    print(f"k * G = {mul_point} k = {k} G = {base_point}")
    # TODO: Convert ProjectivePoint to JacobianPoint
    # TODO: Calculate double-and-add method.
    result = double_and_add(base_point, k)
    print(result)
    assert result == mul_point


def double_and_add(base_point, scalar):
    TWO = FieldInt(2)
    field_value = FieldInt(scalar)
    temp = copy.deepcopy(base_point)
    result = base_point.get_infinity()

    while field_value.value != 0:
        if field_value.value & 1 != 0:
            result += temp
        temp = temp * TWO
        field_value.value >>= 1

    return result


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--stdin", action="store_true", default=False)
    parser.add_argument(
        "--k",
        type=int,
        help="Scalar to multiply the base point by. Defaults to random.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
