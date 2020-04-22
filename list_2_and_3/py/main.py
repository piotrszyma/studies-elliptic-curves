import json
import argparse

import pollard_rho_affine
import affine
import pollard_rho_projective
import projective
import shared


def read_sage_params_from_stdin():
    return json.loads(input())


def run_affine():
    pass


def run_projective():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=["affine", "projective"])
    args = parser.parse_args()
    sage_params = read_sage_params_from_stdin()
    
    print(sage_params)

    base_point = shared.CurveBasePoint(*sage_params["basePoint"][:2])
    field_order = sage_params["fieldOrder"]
    curve_order = sage_params["curveOrder"]
    a, b = sage_params["invariants"]
    
    # RUN FROM DIR /list_2_and_3/py/ !
    # bash ../sage/generate.sh 12 > python3 main.py projective
    # TODO: Run projective or affine based args.type
