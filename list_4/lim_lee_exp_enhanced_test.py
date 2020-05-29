import random
import unittest

import lim_lee_exp_enhanced
import lookup_table_builder
import params_finder
import affine
import field
from affine import AffinePoint, set_curve_params
from shared import CurveBasePoint, CurveParams

AffinePoint = affine.AffinePoint
FieldInt = field.FieldInt


class LimLeeExpEnhancedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        curve_params = CurveParams(
            base_point=CurveBasePoint(172235452673, 488838007757),
            a=236367012452,
            b=74315650609,
            field_order=807368793739,
            curve_order=807369655039,
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
