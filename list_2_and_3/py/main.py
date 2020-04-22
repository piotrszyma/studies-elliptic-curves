import json
import argparse
import timer

import pollard_rho_affine
import affine
import pollard_rho_projective
import projective
import shared


def read_sage_params_from_file(file_path):
    with open(file_path) as f:
        return json.load(f)


def read_sage_params_from_stdin():
    return json.loads(input())


def create_curve_params(raw_json, ec_type):
    a, b = raw_json["invariants"][0], raw_json["invariants"][1]
    base_point = raw_json["basePoint"]
    field_order = raw_json["fieldOrder"]
    curve_order = raw_json["curveOrder"]

    if ec_type == "affine":
        params = affine.CurveParams(
            base_point=affine.CurveBasePoint(
                *base_point[:2],
            ),
            a=a,
            b=b,
            field_order=field_order,
            curve_order=curve_order
        )
    else:
        params = projective.CurveParams(
            base_point=projective.CurveBasePoint(
                *base_point,
            ),
            a=a,
            b=b,
            field_order=field_order,
            curve_order=curve_order
        )
    return params


def run_affine(curve_params):
    params = pollard_rho_affine.generate_params(curve_params)
    instance = pollard_rho_affine.EcAffinePollardRhoDL(params)
    with timer.timeit("PollardRhoDL algorithm"):
        x_found = instance.run()

    print(f"x_found: {x_found}")

    real = curve_params.base_point_y
    # restored = pow(curve_params.g_prim, x_found, params.p)

    # print(f"Real: g_prim^x = {real}, restored: g_prim^x_found {restored}")
    # pollard_rho_affine.run()


def run_projective(curve_params):
    params = pollard_rho_projective.generate_params(curve_params)
    instance = pollard_rho_projective.EcProjectivePollardRhoDL(params)

    with timer.timeit("PollardRhoDL algorithm"):
        x_found = instance.run()

    print(f"x_found: {x_found}")


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

    # RUN FROM DIR /list_2_and_3/py/ !
    # bash ../sage/generate.sh 12 > python3 main.py projective
