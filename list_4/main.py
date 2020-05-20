import argparse
import os
import math

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", type=int, required=True, help='First split')
    parser.add_argument("-v", type=int, required=True, help='Second split.')
    return parser.parse_args()

def split(num, n_chunks):
    """Splits num binary representation into #n chunks of equal size.

    e.g. 
      if the number is X = 1101 0101 1010 
      # of chunks = 3 then as # of bits in X is 12 then yields [0b1101, 0b0101, 0b1010]
    """
    num_bits = math.ceil(math.log(num, 2))
    chunk_bits_size = math.ceil(num_bits / n_chunks)

    mask = int('1' * chunk_bits_size, base =2)
    while num:
      yield num & mask
      num >>= chunk_bits_size

def main():
    args = parse_args()

    u = args.u # in the paper denoted as "h"
    v = args.v # in the paper denoted as "v"

    # Take some g and R, we want to compute g ^ R
    g = int(os.urandom(256//8).hex(), 16)
    R = int(os.urandom(256//8).hex(), 16)
    
    n = math.ceil(math.log(R, 2))  # Number of bits of the exponent.
    a = math.ceil(n / u)  # Number of bits in single slice.

    chunks = [*split(R, u)]
    chunks_of_chunks = [[*split(chunk, v)] for chunk in chunks]

    # First subdivide R into h blocks R_i of size a = math.ceil(n / h)
    import pdb; pdb.set_trace()

    # TODO: calculate g_0, g_1, ..., g_h

    two_to_a = 2 ** a

    g_list = [g] 
    for _ in range(1, h):
      g_list.append(g_list[-1] ** two_to_a)

    assert len(g_list) == h

    

if __name__ == "__main__":
    main()
