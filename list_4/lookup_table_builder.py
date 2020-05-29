# Example usage:
# python3 lookup_table_builder.py -a 74 -b 19 --gx 336972847628 --gy 312067054078 --num-bits 40
import argparse
import math
import pickle
import lim_lee_exp_enhanced
import setup

import affine
import field

AffinePoint = affine.AffinePoint
FieldInt = field.FieldInt


def main(args):
    g = AffinePoint(args.gx, args.gy)
    a = args.a
    b = args.b
    num_bits = args.num_bits
    precomputed_G = lim_lee_exp_enhanced.build_lookup_table(g, num_bits, a, b)

    with open(args.output_path, "wb") as f:
        pickle.dump(precomputed_G, f)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gx", type=int, required=True, help='x of base AffinePoint')
    parser.add_argument("--gy", type=int, required=True, help='y of base AffinePoint')
    parser.add_argument("--num-bits", type=int, required=True, help='Num of bits')
    parser.add_argument("-a", type=int, required=True)
    parser.add_argument("-b", type=int, required=True)
    parser.add_argument("--stdin", action="store_true", default=False)
    parser.add_argument("--path", type=str)
    parser.add_argument("--output-path", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    setup.set_curve_params(args)
    main(args)
