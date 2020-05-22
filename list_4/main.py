import sys
import json
import argparse
import os
import math
import functools
from typing import List

sys.path.append("../list_2_and_3/py")

import affine
import field
import shared

AffinePoint = affine.AffinePoint


def _read_sage_params_from_file(file_path):
    with open(file_path) as f:
        return json.load(f)


def _read_sage_params_from_stdin():
    return json.loads(input())


def _set_curve_params(args):
    if args.stdin:
        raw_json = _read_sage_params_from_stdin()
    else:
        raw_json = _read_sage_params_from_file(args.path)

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
    field.set_modulus(field_order)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", type=int, required=True, help="First split")
    parser.add_argument("-v", type=int, required=True, help="Second split.")
    parser.add_argument("--stdin", action="store_true", default=False)
    parser.add_argument("--path", type=str, default="params_40.json")
    return parser.parse_args()


def split(num, n_chunks):
    """Splits num binary representation into #n chunks of equal size.

    e.g. 
      if the number is X = 1101 0101 1010 
      # of chunks = 3 then as # of bits in X is 12 then yields [0b1101, 0b0101, 0b1010]
    """
    num_bits = math.ceil(math.log(num, 2))
    chunk_bits_size = math.ceil(num_bits / n_chunks)

    mask = int("1" * chunk_bits_size, base=2)
    while num:
        yield num & mask
        num >>= chunk_bits_size


def main():
    args = parse_args()
    _set_curve_params(args)
    u = args.u  # in the paper denoted as "h"
    v = args.v  # in the paper denoted as "v"
    h = u

    # Take some g and R, we want to compute g ^ R
    g = affine.AffinePoint.random()
    R = affine.AffinePoint.get_random_scalar()

    n = math.ceil(math.log(R, 2))  # Number of bits of the exponent.
    a = math.ceil(n / u)  # Number of bits in single slice.

    chunks = [*split(R, u)]
    chunks_of_chunks = [[*split(chunk, v)] for chunk in chunks]

    # First subdivide R into h blocks R_i of size a = math.ceil(n / h)
    two_to_a = 2 ** a

    g_list: List[AffinePoint] = [g]
    for _ in range(1, u):
        g_list.append(g_list[-1] * two_to_a)

    assert len(g_list) == u

    print(f"g_list = {g_list}")

    G = []

    # Calculate G[0][u] for 0 < u < 2**h
    for u in range(1, 2 ** h):
        bin_ids = map(int, bin(u)[2:].zfill(h))
        gs_to_consider = [g_el for g_el, power in zip(g_list, bin_ids) if power == 1]
        G.append(functools.reduce(lambda prev, curr: prev + curr, gs_to_consider))

    # TODO: Calculate G[j][u] for j in 0 < j < v and u in 0 < u < 2**h
    import pdb

    pdb.set_trace()


if __name__ == "__main__":
    main()
