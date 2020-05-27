import argparse
import lim_lee_exp_enhanced

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--r-bits", type=int, help="Number of bits in number.", required=True,
    )
    parser.add_argument(
        "--s-max", type=int, help="Max storage", required=True,
    )
    args = parser.parse_args()
    print(f"Searching for # of bits: {args.r_bits} and max storage: {args.s_max}")
    a, b = lim_lee_exp_enhanced.optimize_parameters(R_bits=args.r_bits, S_max=args.s_max)
    print(f"Found: a: {a} and b: {b}")
