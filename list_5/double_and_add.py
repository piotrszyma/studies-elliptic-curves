import argparse
import random

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
