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


def lim_lee_exp(base, exp, num_of_chunks, num_of_subchunks):
    g = base
    R = exp
    h = num_of_chunks
    v = num_of_subchunks

    # Generate chunks of chunks.
    R_bits = math.ceil(math.log(R, 2))  # Number of bits of the exponent.
    a = math.ceil(R_bits / h)  # Number of bits in single slice.
    b = math.ceil(a / v)  # number of bits in a single slice of slice

    print(
        f"""
Running lim-lee with

l: {R_bits}
h: {h}
v: {v}
a: {a}
b: {b}
"""
    )

    R_str = bin(R)[2:]

    chunks_str = split_str(R_str, a)
    chunks_of_chunks_str = [split_str(chunk_str, b) for chunk_str in chunks_str]

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

    # Calculate G[j][u] for j in 0 < j < v and u in 0 < u < 2**h
    for j in range(1, v):
        exponent = 2 ** (j * b)
        for u in range(1, 2 ** h):  # u from 1 to (2 ** h - 1)
            G[j][u] = G[0][u] * exponent

    # Exponentation
    R_output = AffinePoint.get_infinity()
    for k in range(b):  # k from b - 1 down to 0
        R_output = R_output * 2
        for j in range(v):  # j from v - 1 down to 0
            I_j_k = sum(int(chunks_of_chunks_str[i][j][k]) * (2 ** i) for i in range(h))

            if I_j_k == 0:
                continue

            R_output = R_output + G[j][I_j_k]

    return R_output


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
    num_of_chunks = 10
    num_of_subchunks = 5
    result = lim_lee_exp(base, exp, num_of_chunks, num_of_subchunks)

    expected = base * exp
    assert result == expected
