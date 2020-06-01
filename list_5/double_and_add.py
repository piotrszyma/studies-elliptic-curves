import argparse
import random
from field import FieldInt
import projective
import setup

ProjectivePoint = projective.ProjectivePoint


def main(args):
    curve_params, bit_length = setup.set_curve_params(args)
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


def double_and_add(point, scalar):
    scalar = bin(scalar)[2:]
    TWO = FieldInt(2)
    result = point
    for i in range(len(scalar)-1, -1, -1):
        result = result * TWO
        if scalar[i] == "1":
            result += point
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
