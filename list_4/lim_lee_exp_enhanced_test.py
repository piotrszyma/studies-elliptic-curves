import collections
import unittest
import math
import random

import lim_lee_exp_enhanced
import affine
import projective
import field
from shared import CurveBasePoint, CurveParams

AffinePoint = affine.AffinePoint
FieldInt = field.FieldInt
PrecomputationCase = collections.namedtuple("PrecomputationCase", "R_bits S_max")


def _setup_curve():
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


class LimLeeExpEnhancedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _setup_curve()
        precomputations_to_make = (
            PrecomputationCase(R_bits=512, S_max=100),
            PrecomputationCase(R_bits=256, S_max=500),
            PrecomputationCase(R_bits=256, S_max=5000),
            PrecomputationCase(R_bits=150, S_max=500),
        )
        cls.lookup_tables = {}
        cls.found_a_b = {}
        # Default g, can be override.
        cls.g = AffinePoint(
            5500766647459515102121415383197930788461736082075939483175604378292091762735188389021373228733371700982189946675896443112885738755855474011198072400052059706,
            6196571742070369322997582767211672375614301062212534189301819527848804545012910190274143921663775158543034687203084223424923750245576983362405754170065531174,
        ).convert_to_projective_point()

        for R_bits, S_max in precomputations_to_make:
            a, b = lim_lee_exp_enhanced.optimize_parameters(R_bits=R_bits, S_max=S_max)
            cls.lookup_tables[
                (R_bits, S_max)
            ] = lim_lee_exp_enhanced.build_lookup_table(cls.g, R_bits, a, b)
            cls.found_a_b[(R_bits, S_max)] = (a, b)

    def assert_works_for(self, R, R_bits, S_max):
        real_bits = math.log(R, 2)
        assert real_bits <= R_bits, (
            f"R should have at most {R_bits} bits, " f"but has {real_bits}."
        )
        a, b = self.found_a_b[(R_bits, S_max)]
        precomputed_G = self.lookup_tables[(R_bits, S_max)]
        R_real = self.g * R

        # Act.
        R_output = lim_lee_exp_enhanced.lim_lee_exp_enhanced(
            base=self.g, exp=R, a=a, b=b, precomputed_G=precomputed_G,
        )

        # Assert.
        assert (
            R_output == R_real
        ), f"Calculated R_output = {R_output} should be equal to real g * R = {R_real}"

    def assert_fuzzy_works_for(self, R_bits, S_max, n_runs=10):
        print(f'\nRunning {n_runs} times for R_bits = {R_bits} and S_max = {S_max}')
        for _ in range(n_runs):
            R = random.getrandbits(R_bits)
            with self.subTest(R):
                # Act and assert.
                self.assert_works_for(
                    R=R, R_bits=R_bits, S_max=S_max,
                )

    def test_works_for_storage_size_R_bits_256_s_max_100(self):
        self.assert_fuzzy_works_for(R_bits=512, S_max=100)

    def test_works_for_storage_size_R_bits_256_s_max_500(self):
        self.assert_fuzzy_works_for(R_bits=256, S_max=500)

    def test_works_for_storage_size_R_bits_150_s_max_500(self):
        self.assert_fuzzy_works_for(R_bits=150, S_max=500)

    def test_works_for_storage_size_R_bits_256_s_max_5000(self):
        self.assert_fuzzy_works_for(R_bits=256, S_max=5000)

if __name__ == "__main__":
    unittest.main()
