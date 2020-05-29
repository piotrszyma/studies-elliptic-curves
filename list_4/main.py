import argparse

import affine
import field
import setup
import lim_lee_exp
import lim_lee_exp_enhanced

AffinePoint = affine.AffinePoint
FieldInt = field.FieldInt


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", type=int)
    parser.add_argument("-v", type=int)
    parser.add_argument("-a", type=int)
    parser.add_argument("-b", type=int)
    parser.add_argument("--stdin", action="store_true", default=False)
    parser.add_argument("--path", type=str, default="params_40.json")
    parser.add_argument("--enhanced", action="store_true", default=False)
    parser.add_argument("--gx", type=int, required=True, help='x of base AffinePoint')
    parser.add_argument("--gy", type=int, required=True, help='y of base AffinePoint')
    parser.add_argument(
        "--R", type=int, required=True, help='Value by which to multiply affine point')

    parser.add_argument(
        "--lookups-path", type=str, help="If not provided, will calculate lookups."
    )
    return parser.parse_args()


# python3 main.py -a 185 -b 47 --path params_40.json --enhanced --gx 336972847628 --gy 312067054078 --R 1150191622
def main():
    args = parse_args()
    setup.set_curve_params(args)

    # skalar losowy, dl 520 bitów zredukowany modulo rzad punktu bazowego

    # TODO: Take from input or something?

    # -    g = AffinePoint(336972847628, 312067054078)
    # -    R = FieldInt(value=1150191622)
    g = AffinePoint(args.gx, args.gy)
    R = FieldInt(value=args.R)

    if args.enhanced:
        R_output = lim_lee_exp_enhanced.lim_lee_exp_enhanced(g, R, args.a, args.b)
    else:
        v = args.v  # in the paper denoted as "v"
        h = args.u
        R_output = lim_lee_exp.lim_lee_exp(g, R, h, v)

    R_real = g * R.value

    assert (
        R_output == R_real
    ), f"Calculated R_output = {R_output} should be equal to real g * R = {R_real}"

    print("Successfully calculated.")


if __name__ == "__main__":
    main()
