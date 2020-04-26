import json
import argparse
import timer

import pollard_rho_affine
import affine
import pollard_rho_projective
import projective
import field
import shared


def read_sage_params_from_file(file_path):
    with open(file_path) as f:
        return json.load(f)


def read_sage_params_from_stdin():
    return json.loads(input())


def create_curve_params(raw_json, ec_type):
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
    projective.set_curve_params(curve_params)
    field.set_modulus(field_order)
    return curve_params


def _print_results(params: shared.CurveParams, x_found):
    mul_calculated = x_found * params.base_point
    print(f"x_found * base_point = {mul_calculated}, mul_real = {params.mul_point}")
    assert mul_calculated == params.mul_point, "Failed to find point."
    print("Successfully found point!")


def run_affine(curve_params):
    params = pollard_rho_affine.generate_params(curve_params)
    instance = pollard_rho_affine.EcAffinePollardRhoDL(params)
    with timer.timeit("PollardRhoDL algorithm on affine coordinates."):
        x_found = instance.run()
    _print_results(params, x_found)


def run_projective(curve_params):
    params = pollard_rho_projective.generate_params(curve_params)
    instance = pollard_rho_projective.EcProjectivePollardRhoDL(params)
    with timer.timeit("PollardRhoDL algorithm on projective coordinates."):
        x_found = instance.run()
    _print_results(params, x_found)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["affine", "projective"])
    parser.add_argument("--stdin", action="store_true", default=False)
    parser.add_argument("--path", type=str, default="sage_params.json")
    args = parser.parse_args()

    if args.stdin:
        raw_json = read_sage_params_from_stdin()
    else:
        raw_json = read_sage_params_from_file(args.path)

    curve_params = create_curve_params(raw_json, args.type)
    print(f"Running for {curve_params}")

    if args.type == "affine":
        run_affine(curve_params)
    else:
        run_projective(curve_params)
