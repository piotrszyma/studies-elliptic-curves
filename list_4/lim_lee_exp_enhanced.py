from tqdm import tqdm

import math
import affine
import field
import utils
from affine import set_curve_params
from shared import CurveBasePoint, CurveParams


AffinePoint = affine.AffinePoint
FieldInt = field.FieldInt
IntWithBinIndex = utils.IntWithBinIndex


def split_str(num_str, bits_in_chunk):
    rfilled_size = math.ceil(len(num_str) / bits_in_chunk) * bits_in_chunk
    num_str = num_str.zfill(rfilled_size)
    splitted = []
    for idx in range(0, len(num_str), bits_in_chunk):
        splitted.append(num_str[idx : idx + bits_in_chunk])
    return splitted[::-1]


def build_lookup_table(g, num_bits, a, b):
    print(
        f"""
    Building lookup table for
    g: {g}
    num_bits: {num_bits}
    a: {a}
    b: {b}
    """
    )
    h, v, a_last, v_last, b_last = compute_parameters(num_bits, a, b)

    # Prepare list of g_i.
    g_list = [g * (2 ** (i * a)) for i in range(h)]

    # Generate G two dim table.
    G = {idx: {} for idx in range(v)}

    # Calculate G[0][u] for 0 < u < 2**h
    for u in range(1, 2 ** h):  # u from 1 to (2 ** h - 1)
        u_bits = bin(u)[2:].zfill(h)
        r_bits = g_list[::-1]
        muls = [r for u, r in zip(u_bits, r_bits) if u == "1"]
        G[0][u] = AffinePoint.get_infinity()
        for mul in muls:
            G[0][u] += mul

    assert len(G[0]) == len(range(1, 2 ** h))

    for j in range(1, v_last):
        exponent = 2 ** (j * b)
        for u in range(1, 2 ** h):  # u from 1 to (2 ** h - 1)
            G[j][u] = G[0][u] * exponent

    for j in range(0, v - v_last):
        exponent = 2 ** ((v_last + j) * b)
        for u in range(1, 2 ** (h - 1)):
            G[v_last + j][u] = G[0][u] * exponent

    lookup_table_size = sum(1 for row in G.values() for _ in row)

    print(f"Look-up table size: {lookup_table_size}")

    return G


def lim_lee_exp_enhanced(base, exp, a, b, precomputed_G=None):
    R = exp
    # Generate chunks of chunks.
    R_bits = math.ceil(math.log(R, 2))  # Number of bits of the exponent.
    R_str = bin(R)[2:]
    h, v, a_last, v_last, b_last = compute_parameters(R_bits, a, b)
    G = precomputed_G if precomputed_G else build_lookup_table(base, R_bits, a, b)

    chunks_str = split_str(R_str, a)
    # chunks_str[-1] = chunks_str[-1][-a_last:]

    chunks_of_chunks_str = [split_str(chunk_str, b) for chunk_str in chunks_str]
    # chunks_of_chunks_str.append(split_str(chunks_str[-1], v_last))

    # Exponentation
    R_output = AffinePoint.get_infinity()
    no_of_additions = 0
    no_of_mutliplications = 0

    for k in range(b):
        R_output = R_output * 2
        no_of_mutliplications += 1
        for j in range(v):
            I_j_k = sum(int(chunks_of_chunks_str[i][j][k]) * (2 ** i) for i in range(h))

            if I_j_k == 0:
                continue

            R_output = R_output + G[j][I_j_k]
            no_of_additions += 1

    print(f"# of Additions: {no_of_additions}")
    print(f"# of Multiplications: {no_of_mutliplications}")
    return R_output


def optimize_parameters(R_bits, S_max):
    curr_S = math.inf
    curr_no_of_operations = math.inf
    best_a = None
    best_b = None

    for a in tqdm(range(1, R_bits)):
        for b in range(1, a):
            h, v, a_last, v_last, b_last = compute_parameters(R_bits, a, b)
            S = compute_storage_requirement(h, v, v_last)
            if S < S_max:
                no_of_operations = compute_number_of_operations(a, b, a_last, h)
                if no_of_operations < curr_no_of_operations:
                    curr_S = S
                    curr_no_of_operations = no_of_operations
                    best_a = a
                    best_b = b

    print(f"Storage used: {curr_S}")
    print(f"Operations performed {curr_no_of_operations}")
    print(f"a: {best_a}, b: {best_b}")
    return best_a, best_b


def compute_parameters(R_bits, a, b):

    h = math.ceil(R_bits / a)
    v = math.ceil(a / b)

    a_last = R_bits - a * (h - 1)

    v_last = math.ceil(a_last / b)

    b_last = a_last - b * (v_last - 1)

    return h, v, a_last, v_last, b_last


def compute_number_of_operations(a, b, a_last, h):
    squarings = b - 1
    mul_left = (a - a_last) * ((2 ** (h - 1) - 1) / (2 ** (h - 1)))
    mul_right = a_last * ((2 ** h - 1) / (2 ** h)) - 1
    multiplications = mul_left + mul_right
    return squarings + multiplications


def compute_storage_requirement(h, v, v_last):
    return (2 ** h - 1) * v_last + (2 ** (h - 1) - 1) * (v - v_last)


if __name__ == "__main__":
    curve_params = CurveParams(
        base_point=CurveBasePoint(
            x=2661740802050217063228768716723360960729859168756973147706671368418802944996427808491545080627771902352094241225065558662157113545570916814161637315895999846,
            y=3757180025770020463545507224491183603594455134769762486694567779615544477440556316691234405012945539562144444537289428522585666729196580810124344277578376784,
            z=1,
        ),
        a=-3,
        b=1093849038073734274511112390766805569936207598951683748994586394495953116150735016013708737573759623248592132296706313309438452531591012912142327488478985984,
        curve_order=6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449,
        field_order=6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151,
    )
    set_curve_params(curve_params)
    field.set_modulus(curve_params.field_order)
    base = AffinePoint(
        5500766647459515102121415383197930788461736082075939483175604378292091762735188389021373228733371700982189946675896443112885738755855474011198072400052059706,
        6196571742070369322997582767211672375614301062212534189301819527848804545012910190274143921663775158543034687203084223424923750245576983362405754170065531174,
    )
    exp = 2767201098028965716409203771940239753707949971455379335681895958567502012410

    a = 26
    b = 6
    result = lim_lee_exp_enhanced(base, exp, a, b)

    expected = base * exp
    assert result == expected, "Failed to calculate."
    print("Calculated.")
