import unittest

import lim_lee_exp_enhanced
import affine
import field
from affine import set_curve_params
from shared import CurveBasePoint, CurveParams

AffinePoint = affine.AffinePoint
FieldInt = field.FieldInt


class LimLeeExpEnhancedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
        params = (
            (256, 100),
            (256, 500),
        )
        cls.lookup_tables = {}
        cls.found_a_b = {}
        cls.g = AffinePoint(178539744208, 550836080620)

        for R_bits, S_max in params:
            a, b = lim_lee_exp_enhanced.optimize_parameters(R_bits=R_bits, S_max=S_max)
            cls.lookup_tables[
                (R_bits, S_max)
            ] = lim_lee_exp_enhanced.build_lookup_table(cls.g, R_bits, a, b)
            cls.found_a_b[(R_bits, S_max)] = (a, b)

    def test_works_for_storage_size_R_bits_256_s_max_100(self):
        # Arrange.
        R = 2767201098028965716409203771940239753707949971455379335681895958567502012410
        a, b = self.found_a_b[(256, 100)]
        precomputed_G = self.lookup_tables[(256, 100)]
        R_real = self.g * R

        # Act.
        R_output = lim_lee_exp_enhanced.lim_lee_exp_enhanced(
            base=self.g, exp=R, a=a, b=b, precomputed_G=precomputed_G,
        )

        # Assert.
        assert (
            R_output == R_real
        ), f"Calculated R_output = {R_output} should be equal to real g * R = {R_real}"

    def test_works_for_storage_size_R_bits_256_s_max_500(self):
        # Arrange.
        R = 2767201098028965716409203771940239753707949971455379335681895958567502012410
        a, b = self.found_a_b[(256, 500)]
        precomputed_G = self.lookup_tables[(256, 500)]
        R_real = self.g * R

        # Act.
        R_output = lim_lee_exp_enhanced.lim_lee_exp_enhanced(
            base=self.g, exp=R, a=a, b=b, precomputed_G=precomputed_G,
        )

        # Assert.
        assert (
            R_output == R_real
        ), f"Calculated R_output = {R_output} should be equal to real g * R = {R_real}"


if __name__ == "__main__":
    unittest.main()
