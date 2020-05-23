import json
import argparse
import math
import random
import functools
from typing import List

import affine
import field
import shared
import copy
import utils

AffinePoint = affine.AffinePoint
FieldInt = field.FieldInt
IntWithBinIndex = utils.IntWithBinIndex


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


def split(num, n_of_chunks):
    """Splits num binary representation into # n_of_chunks of equal size.

    e.g. 
      if the number is X = 1101 0101 1010 
      # of chunks = 3 then as # of bits in X is 12 then yields [0b1101, 0b0101, 0b1010]
    """

    n_of_bits_all = math.ceil(math.log(num, 2))  # Number of bits of the exponent.
    # number of bits in a single slice of slice
    n_of_bits_chunk = math.ceil(n_of_bits_all / n_of_chunks)

    mask = int("1" * n_of_bits_chunk, base=2)
    num = copy.deepcopy(num)
    for _ in range(n_of_chunks):
        yield IntWithBinIndex(num & mask)
        num >>= n_of_bits_chunk


def split_str(num_str, n_of_chunks):
    lpad = (math.ceil(len(num_str) / n_of_chunks) * n_of_chunks) - len(num_str)
    num_str = "0" * lpad + num_str
    chunk_size = len(num_str) // n_of_chunks

    splitted = []
    for idx in range(0, len(num_str), chunk_size):
        splitted.append(num_str[idx : idx + chunk_size])
    return splitted[::-1]


def main():
    args = parse_args()
    _set_curve_params(args)
    u = args.u  # in the paper denoted as "h"
    v = args.v  # in the paper denoted as "v"
    h = u

    random.seed(0)  # For repeated randomness.

    # Take some g and R, we want to compute g ^ R
    g = 122
    R = 231
    # g = AffinePoint(336972847628, 312067054078)
    # R = FieldInt(value=1150191622)

    R_bits = math.ceil(math.log(R, 2))  # Number of bits of the exponent.
    a = math.ceil(R_bits / h)  # Number of bits in single slice.
    b = math.ceil(a / v)  # number of bits in a single slice of slice

    R_str = bin(R)[2:]

    chunks_str = split_str(R_str, h)
    chunks_of_chunks_str = [split_str(chunk_str, v) for chunk_str in chunks_str]

    chunks = [int(e, base=2) for e in chunks_str]
    chunks_of_chunks = []
    for chunk_str in chunks_of_chunks_str:
        chunks_of_chunks.append([int(e, base=2) for e in chunk_str])

    assert len(chunks) == h
    assert R == sum(e_i * (2 ** (i * a)) for i, e_i in enumerate(chunks))
    for i, chunk in enumerate(chunks):
        assert chunk == sum(chunks_of_chunks[i][j] * (2 ** (j * b)) for j in range(v))

    g_list = []
    for i in range(h):
        g_list.append(g ** (2 ** (i * a)))

    assert len(g_list) == h

    G = {idx: {} for idx in range(v)}
    # Calculate G[0][u] for 0 < u < 2**h
    for u in range(1, 2 ** h):  # u from 1 to (2 ** h - 1)
        u_bits = bin(u)[2:].zfill(h)
        r_bits = g_list[::-1]
        muls = [r for u, r in zip(u_bits, r_bits) if u == '1']
        G[0][u] = 1
        for mul in muls:
            G[0][u] *= mul

    assert len(G[0]) == len(range(1, 2 ** h))

    # Calculate G[j][u] for j in 0 < j < v and u in 0 < u < 2**h
    for j in range(1, v):
        # exponent = field.FieldInt(2) * (field.FieldInt(j) * b_field_int)
        exponent = 2 ** (j * b)
        for u in range(1, 2 ** h):  # u from 1 to (2 ** h - 1)
            G[j][u] = G[0][u] ** exponent

    # Exponentation
    R_output = 1
    for k in range(b - 1, -1, -1):  # k from b - 1 down to 0
        R_output = R_output ** 2
        for j in range(v - 1, -1, -1):  # j from v - 1 down to 0
            I_j_k = sum(int(chunks_of_chunks_str[i][j][::-1][k]) * (2 ** i) for i in range(h))

            if I_j_k == 0:
                print("Warning, I_j_k returned 0...")
                continue
            R_output = R_output * G[j][I_j_k]

    R_real = g ** R
    assert (
        R_output == R_real
    ), f"Calculated R_output = {R_output} should be equal to real g * R = {R_real}"


if __name__ == "__main__":
    main()
