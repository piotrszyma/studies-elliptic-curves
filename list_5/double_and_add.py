import argparse
import random
from field import FieldInt
import jacobi
import copy
import setup

JacobiPoint = jacobi.JacobiPoint


def main(args):
    curve_params, bit_length = setup.set_curve_params(args)
    print(curve_params)
    k = args.k if args.k is not None else random.getrandbits(bit_length)
    base_point = JacobiPoint.base()
    mul_point = base_point.convert_to_affine_point() * k
    print(f"k * G = {mul_point} k = {k} G = {base_point}")
    result = double_and_add(base_point, k)
    assert result.convert_to_affine_point() == mul_point, "Failed to compute k * G."
    print("Successfully computed k * G.")


def double_and_add(base_point, scalar):
    TWO = FieldInt(2)
    temp = copy.deepcopy(base_point)
    result = base_point.get_infinity()

    while scalar != 0:
        if scalar & 1 != 0:
            result += temp
        temp = temp * TWO
        scalar >>= 1

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
