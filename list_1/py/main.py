"""Elliptic curves tasks implementation in python.

Useful for test cases generation.

+ generate pollard's rho test case
  python3 main.py --genparams --nbits 40 > /tmp/params

  will stdout g_prim, p, p_prim, y line by line

+ generate and run pollard's rho algorithm
  python3 main.py --nbits 40

  will generate and run pollard's rho algorithm

+ run pollard's rho algorithm on already generated params
  python3 ../../py/main.py --fromstdin -n 40 < /tmp/params
"""
import argparse

from algorithms import pollard_rho
from utils import primegen

parser = argparse.ArgumentParser()
parser.add_argument("--genparams", "-g", action="store_true", default=False)
parser.add_argument("--nbits", "-n", type=int, default=40)
parser.add_argument("--fromstdin", "-in", action="store_true", default=False)
parser.add_argument("--openssl", "-o", action="store_true", default=False)


def main():
    args = parser.parse_args()

    if args.fromstdin:
        params = pollard_rho.PollardRhoDLParams(
            g_prim=int(input()), p=int(input()), p_prim=int(input()), y=int(input()),
        )
    else:
        generate_prime_fn = (
            primegen.random_safe_prime_from_openssl
            if args.openssl
            else primegen.random_safe_prime_from_gensafeprime
        )

        prime = generate_prime_fn(args.nbits)
        params = pollard_rho.generate_params(prime)

    if args.genparams:
        print(params.g_prim)
        print(params.p)
        print(params.p_prim)
        print(params.y)
        return
    else:
        print(f"Running for {params}")

        x_found = pollard_rho.PollardRhoDL(params).run()

        print(f"x_found: {x_found}")
        print(f"g_prim ^ x_found % p: {pow(params.g_prim, x_found, params.p)}")
        print(f"y: {params.y}")
        return


if __name__ == "__main__":
    main()
