import math
import affine
import field
import utils

AffinePoint = affine.AffinePoint
FieldInt = field.FieldInt
IntWithBinIndex = utils.IntWithBinIndex


def split_str(num_str, n_of_chunks):
    lpad = (math.ceil(len(num_str) / n_of_chunks) * n_of_chunks) - len(num_str)
    num_str = "0" * lpad + num_str
    chunk_size = len(num_str) // n_of_chunks

    splitted = []
    for idx in range(0, len(num_str), chunk_size):
        splitted.append(num_str[idx : idx + chunk_size])
    return splitted[::-1]


def lim_lee_exp_enhanced(base, exp, a, b):
    g = base
    R = exp
    
    # Generate chunks of chunks.
    R_bits = math.ceil(math.log(R, 2))  # Number of bits of the exponent.
    R_str = bin(R)[2:]

    h = math.ceil(R_bits / a)
    v = math.ceil(a / b)

    a_last = R_bits - a * (h - 1)

    v_last = math.ceil(a_last / b)

    b_last = a_last - b * (v_last - 1)

    print(f"""
Running lim-lee enhanced (v2) with

l: {R_bits}
h: {h}
v: {v}
v_last: {v_last}
a: {a}
a_last: {a_last}
b: {b}
b_last: {b_last}
""")

    chunks_str = split_str(R_str, h)
    chunks_str[-1] = chunks_str[-1][-a_last:]

    chunks_of_chunks_str = [split_str(chunk_str, v) for chunk_str in chunks_str[:-1]]
    chunks_of_chunks_str.append(split_str(chunks_str[-1], v_last))

    # chunks = [int(e, base=2) for e in chunks_str]
    # chunks_of_chunks = []
    # for chunk_str in chunks_of_chunks_str:
    #     chunks_of_chunks.append([int(e, base=2) for e in chunk_str])

    # assert len(chunks) == h
    # assert R == sum(e_i * (2 ** (i * a)) for i, e_i in enumerate(chunks))
    # for i, chunk in enumerate(chunks):
    #     assert chunk == sum(chunks_of_chunks[i][j] * (2 ** (j * b)) for j in range(v))

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
    for k in range(b - 1, -1, -1):  # k from b - 1 down to 0
        R_output = R_output * 2
        for j in range(v - 1, -1, -1):  # j from v - 1 down to 0
            I_j_k = 0
            for i in range(h):
                try:
                    I_j_k += int(chunks_of_chunks_str[i][j][::-1][k]) * (2 ** i)
                except IndexError:
                    pass

            if I_j_k == 0:
                print("Warning, I_j_k returned 0...")
                continue
            R_output = R_output + G[j][I_j_k]

    return R_output
