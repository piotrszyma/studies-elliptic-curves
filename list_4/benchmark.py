import collections
import unittest
import math
import random

import lim_lee_exp_enhanced
import affine
import projective
import time
import field
from shared import CurveBasePoint, CurveParams
from projective import ProjectivePoint
from affine import AffinePoint
from lim_lee_exp_enhanced import lim_lee_exp_enhanced, optimize_parameters

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
affine.set_curve_params(curve_params)
projective.set_curve_params(curve_params)
field.set_modulus(curve_params.field_order)


def normal_mult(P, n):
    adding = 0
    mult = 0
    start = time.time()
    result = ProjectivePoint.get_infinity()

    temp = P
    while n != 0:
        if n & 1 != 0:
            result += temp
            adding += 1
        temp *= 2
        mult += 1
        n >>= 1
    print("Normal:", time.time() - start)
    print("Additions:", adding)
    print("Multiplications:", mult)
    return result



def main():
		
	base = ProjectivePoint(
		5500766647459515102121415383197930788461736082075939483175604378292091762735188389021373228733371700982189946675896443112885738755855474011198072400052059706,
		6196571742070369322997582767211672375614301062212534189301819527848804545012910190274143921663775158543034687203084223424923750245576983362405754170065531174,
		1
	)
		# base = base.convert_to_projective_point()
	exp = 2767201098028965716409203771940239753707949971455379335681895958567502012410

	normal_mult(base, exp)
	R_bits = len(bin(exp)[2:])
	S_max = 100
	a, b = optimize_parameters(R_bits, S_max)
	lim_lee_exp_enhanced(base, exp, a, b)


if __name__ == "__main__":
	main()