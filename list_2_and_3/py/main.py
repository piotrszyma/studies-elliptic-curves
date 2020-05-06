import json
import argparse
import timer
import random

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


def run_affine(curve_params, value_to_find, time_only):
    params = pollard_rho_affine.generate_params(curve_params, value_to_find)
    instance = pollard_rho_affine.EcAffinePollardRhoDL(params)

    with timer.timeit("PollardRhoDL algorithm on affine coordinates.", time_only):
        x_found = instance.run()

    if not time_only:
        _print_results(params, x_found)


def run_projective(curve_params, value_to_find, time_only):
    params = pollard_rho_projective.generate_params(curve_params, value_to_find)
    instance = pollard_rho_projective.EcProjectivePollardRhoDL(params)

    with timer.timeit("PollardRhoDL algorithm on projective coordinates.", time_only):
        x_found = instance.run()

    if not time_only:
        _print_results(params, x_found)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["affine", "projective"])
    parser.add_argument("--stdin", action="store_true", default=False)
    parser.add_argument("--profiler", action="store_true", default=False)
    parser.add_argument("--time_only", action="store_true", default=False)
    parser.add_argument("--path", type=str, default="sage_params.json")
    parser.add_argument("--value_to_find", type=int)
    args = parser.parse_args()

    if args.stdin:
        raw_json = read_sage_params_from_stdin()
    else:
        raw_json = read_sage_params_from_file(args.path)

    curve_params = create_curve_params(raw_json, args.type)

    value_to_find = args.value_to_find or random.randint(2, curve_params.curve_order)

    if not args.time_only:
        print(f"Running for {curve_params} and value_to_find={value_to_find}")

    if args.profiler:
        import cProfile

        pr = cProfile.Profile()
        pr.enable()

    if args.type == "affine":
        run_affine(curve_params, value_to_find, args.time_only)
    else:
        run_projective(curve_params, value_to_find, args.time_only)

    if args.profiler:
        pr.disable()
        pr.print_stats()
