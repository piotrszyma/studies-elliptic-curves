import pdb
import sys
import json
import argparse
import os
import math
import random
import functools
from typing import List

sys.path.append("../list_2_and_3/py")

import affine
import field
import shared
import copy

AffinePoint = affine.AffinePoint
FieldInt = field.FieldInt


class IntWithBinIndex(int):
    def __getitem__(self, value):
        try:
            return int(bin(self)[2:][value])
        except IndexError:
            return 0


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
    num_bits = len(bin(num)[2:])
    # num_bits = len(num)
    chunk_bits_size = math.ceil(num_bits / n_chunks)
    mask = int("1" * chunk_bits_size, base=2)
    real_n_chunks = 0
    num = copy.deepcopy(num)
    while num:
        # yield bin(num & mask)[2:]
        yield IntWithBinIndex(num & mask)
        real_n_chunks += 1
        num >>= chunk_bits_size

    while real_n_chunks != n_chunks:
        yield IntWithBinIndex(0)
        real_n_chunks += 1


def main():
    args = parse_args()
    _set_curve_params(args)
    u = args.u  # in the paper denoted as "h"
    v = args.v  # in the paper denoted as "v"
    h = u

    random.seed(0)  # For repeated randomness.

    # Take some g and R, we want to compute g ^ R
    g = affine.AffinePoint.random()
    # g = AffinePoint(336972847628, 312067054078)
    R = affine.AffinePoint.get_random_scalar()
    # R = FieldInt(value=1150191622)

    l = math.ceil(math.log(R, 2))  # Number of bits of the exponent.
    a = math.ceil(l / h)  # Number of bits in single slice.
    b = math.ceil(a / v)

    chunks = [*split(R, u)]
    assert len(chunks) == h

    chunks_of_chunks = [[*split(chunk, v)] for chunk in chunks]

    assert all(len(subchunk) <= v for subchunk in chunks_of_chunks)

    # First subdivide R into h blocks R_i of size a = math.ceil(l / h)
    two_to_a = 2 ** a

    g_list: List[AffinePoint] = [g]
    for _ in range(1, u):
        g_list.append(g_list[-1] * two_to_a)

    assert len(g_list) == u

    G = {idx: {} for idx in range(v)}
    # Calculate G[0][u] for 0 < u < 2**h
    for u in range(1, 2 ** h):  # u from 1 to (2 ** h - 1)
        bin_ids = map(int, bin(u)[2:].zfill(h))
        gs_to_consider = [r_i for r_i, u_i in zip(g_list, bin_ids) if u_i == 1]
        G[0][u] = functools.reduce(lambda prev, curr: prev + curr, gs_to_consider)

    assert len(G[0]) == len(range(1, 2 ** h))

    # Calculate G[j][u] for j in 0 < j < v and u in 0 < u < 2**h
    for j in range(1, v):
        # exponent = field.FieldInt(2) * (field.FieldInt(j) * b_field_int)
        exponent = pow(2, (j * b), field.MODULUS)
        for u in range(1, 2 ** h):  # u from 1 to (2 ** h - 1)
            G[j][u] = (G[j - 1][u] * exponent)
        
        assert len(G[j]) == len(range(1, 2 ** h))
        
    # Exponentation
    e = chunks_of_chunks
    R_output = AffinePoint.get_base_point()
    for k in range(b - 1, -1, -1):  # k from b - 1 down to 0
        R_output = R_output * 2
        for j in range(v - 1, -1, -1):  # j from v - 1 down to 0
            I_j_k = sum(e[i][j][k] * (2 ** i) for i in range(h))

            if I_j_k == 0:
                print('Warning, I_j_k returned 0...')
                continue
            R_output = R_output + G[j][I_j_k]

    R_real = g * R.value
    assert (
        R_output == R_real
    ), f"Calculated R_output = {R_output} should be equal to real g * R = {R_real}"


if __name__ == "__main__":
    main()
