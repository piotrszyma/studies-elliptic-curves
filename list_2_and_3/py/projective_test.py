import unittest
from field import FieldInt

from affine import AffinePoint
from projective import ProjectivePoint, set_curve_params, CurveBasePoint, CurveParams


class ProjectivePointTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        set_curve_params(
            CurveParams(
                base_point=CurveBasePoint(172235452673, 488838007757, 1),
                a=236367012452,
                b=74315650609,
                field_order=807368793739,
                curve_order=807369655039,
            )
        )


class TestProjectivePointConversion(ProjectivePointTestCase):
    def test_conversion_to_affine_and_back(self):
        # Arrange.
        projective_point = ProjectivePoint(2928, 42354, 1)
        # Act.
        affine_point = projective_point.convert_to_affine_point()
        projective_point_from_affine = affine_point.convert_to_projective_point()
        # Assert.
        self.assertEqual(projective_point, projective_point_from_affine)


class TestProjectivePointMultiplicationByScalar(ProjectivePointTestCase):
    def test_point_at_infinitity_times_scalar_should_be_infinity(self):
        # Arrange.
        point_at_inf = ProjectivePoint.get_infinity()
        modulus = ProjectivePoint._curve_params.field_order
        # Act.
        result = point_at_inf * FieldInt(2, modulus)

        # Assert.
        self.assertEqual(result, point_at_inf)

    def test_point_with_y_equal_zero_multiplied_should_be_infinity(self):
        # Arrange.
        # Ugly sets y to 0 without respecting x.
        modulus = ProjectivePoint._curve_params.field_order
        point_with_y_zero = ProjectivePoint(2, 0, 1)

        # Act.
        result = point_with_y_zero * FieldInt(2, modulus)
        
        # Assert.
        self.assertTrue(result.is_infinity())


class TestProjectivePointAddition(ProjectivePointTestCase):

    def test_point_at_infinity_plus_other_should_be_that_other(self):
        # Arrange.
        point = AffinePoint(1234, 5678)
        projective_point = point.convert_to_projective_point()

        point_at_inf = ProjectivePoint.get_infinity()

        # Act.
        result_rhs = projective_point + point_at_inf
        result_lhs = point_at_inf + projective_point

        # Assert.
        self.assertEqual(result_lhs, result_rhs)
        self.assertEqual(result_rhs, projective_point)

    def test_two_points_with_same_x_should_sum_to_infinity(self):
        # Arrange.
        # Ugly sets xs to same value.
        point_1 = ProjectivePoint(1234, 1234, 2)
        point_2 = ProjectivePoint(1234, 5678, 2)

        # Act.
        result = point_1 + point_2

        # Assert.
        self.assertEqual(result, ProjectivePoint.get_infinity())

    def test_two_points_with_same_x_and_same_y(self):
        # Arrange.
        point_1 = ProjectivePoint(172235452673, 488838007757, 1)
        point_2 = ProjectivePoint(172235452673, 488838007757, 1)
        # Act.
        result = point_1 + point_2

        # Assert.
        result = result.convert_to_affine_point()
        self.assertEqual(result, AffinePoint(215387987039, 765000578277))

    def test_mul(self):
        # Arrange.
        point = AffinePoint(172235452673, 488838007757).convert_to_projective_point()
        modulo = point._curve_params.field_order

        # Act.
        point_mul_0 =  FieldInt(2, modulo) * point
        point_mul_1 = point * FieldInt(2137, modulo)
        point_mul_2 = FieldInt(741274052018, modulo) * point
        point_mul_3 = point * FieldInt(649074375334, modulo)
        
        # Assert.
        self.assertEqual(
            AffinePoint(215387987039, 765000578277),
            point_mul_0.convert_to_affine_point()
        )
        self.assertEqual(
            AffinePoint(464122625441, 361301908555),
            point_mul_1.convert_to_affine_point()
        )
        self.assertEqual(
            AffinePoint(702787153408, 513816894152),
            point_mul_2.convert_to_affine_point()
        )
        self.assertEqual(
            AffinePoint(748235734737, 753279782927),
            point_mul_3.convert_to_affine_point()
        )

    def test_add(self):
        # Arrange.
        point_1 = AffinePoint(172235452673, 488838007757).convert_to_projective_point()
        point_2 = AffinePoint(748235734737, 753279782927).convert_to_projective_point()

        # Act.
        point_add_1 = point_1 + point_2
        point_add_2 = point_1 + point_1

        # Assert.
        self.assertEqual(
            AffinePoint(198482119007, 191241681320),
            point_add_1.convert_to_affine_point())
        self.assertEqual(
            AffinePoint(215387987039, 765000578277),
            point_add_2.convert_to_affine_point()
        )

    def test_mix_of_add_and_mul(self):
        # Arrange.
        point = AffinePoint(172235452673, 488838007757).convert_to_projective_point()
        modulo = point._curve_params.field_order

        # Act.
        two_mul_point = FieldInt(2, modulo) * point
        point_add_point = point + point

        # Assert.
        two_mul_point = two_mul_point.convert_to_affine_point()
        point_add_point = point_add_point.convert_to_affine_point()

        self.assertEqual(two_mul_point, AffinePoint(215387987039, 765000578277))
        self.assertEqual(two_mul_point, point_add_point)

    # def test_uga_buga(self):
    #     value = ProjectivePoint(388012790166, 14292500247, 467443641221)
    #     alpha = 2
    #     beta = 2
    #     base_point = ProjectivePoint(172235452673, 488838007757, 1)
    #     mul_point = ProjectivePoint(142354355405, 341203862054, 718281879040)
    #     modulo = value._curve_params.field_order
    #     left = alpha * base_point
    #     right = beta * mul_point
    #     value_new = left + right
    #     import pdb; pdb.set_trace()
    #     assert value == value_new


if __name__ == "__main__":
    unittest.main()
