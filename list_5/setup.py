import json
import shared

import projective
import field
import affine
import jacobi


def _read_sage_params_from_file(file_path):
    with open(file_path) as f:
        return json.load(f)


def _read_sage_params_from_stdin():
    return json.loads(input())


def set_curve_params(args):
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
    projective.set_curve_params(curve_params)
    affine.set_curve_params(curve_params)
    jacobi.set_curve_params(curve_params)
    field.set_modulus(field_order)
    return curve_params, int(raw_json["bitLength"])
