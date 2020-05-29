from tqdm import tqdm

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
        splitted.append(num_str[idx: idx + chunk_size])
    return splitted[::-1]


def build_lookup_table(g, num_bits, a, b):
    print(f"""
    Building lookup table for
    g: {g}
    num_bits: {num_bits}
    a: {a}
    b: {b}
    """)
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

    return G


def lim_lee_exp_enhanced(base, exp, a, b, precomputed_G=None):
    R = exp
    # Generate chunks of chunks.
    R_bits = math.ceil(math.log(R, 2))  # Number of bits of the exponent.
    R_str = bin(R)[2:]
    h, v, a_last, v_last, b_last = compute_parameters(R_bits, a, b)
    G = precomputed_G if precomputed_G else build_lookup_table(base, R_bits, a, b)

    chunks_str = split_str(R_str, h)
    chunks_str[-1] = chunks_str[-1][-a_last:]

    chunks_of_chunks_str = [split_str(chunk_str, v) for chunk_str in chunks_str[:-1]]
    chunks_of_chunks_str.append(split_str(chunks_str[-1], v_last))

    # Exponentation
    R_output = AffinePoint.get_infinity()
    no_of_additions = 0
    no_of_mutliplications = 0

    for k in range(b - 1, -1, -1):  # k from b - 1 down to 0
        R_output = R_output * 2
        no_of_mutliplications += 1
        for j in range(v - 1, -1, -1):  # j from v - 1 down to 0
            I_j_k = 0
            for i in range(h):
                try:
                    I_j_k += int(chunks_of_chunks_str[i][j][::-1][k]) * (2 ** i)
                except IndexError:
                    pass

            if I_j_k == 0:
                # print("Warning, I_j_k returned 0...")
                continue

            try:
                R_output = R_output + G[j][I_j_k]
            except IndexError:
                pass
            else:
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
