import unittest

from affine import AffinePoint  # , set_curve_params, CurveBasePoint, CurveParams
from projective import ProjectivePoint, set_curve_params, CurveBasePoint, CurveParams


class ProjectivePointTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        set_curve_params(
            CurveParams(
                base_point=CurveBasePoint(2928, 42354, 1),
                a=40798,
                b=14047,
                field_order=62071,
                curve_order=62039,
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

        # Act.
        result = point_at_inf * 2

        # Assert.
        self.assertEqual(result, point_at_inf)

    def test_point_with_y_equal_zero_multiplied_should_be_infinity(self):
        # Arrange.
        # Ugly sets y to 0 without respecting x.
        point_with_y_zero = ProjectivePoint(0, 0)

        # Act.
        result = point_with_y_zero * 2

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

    # def test_two_points_with_same_x_should_sum_to_infinity(self):
    #     # Arrange.
    #     # Ugly sets xs to same value.
    #     point_1 = AffinePoint(1234, 1234)
    #     point_2 = AffinePoint(1234, 5678)

    #     # Act.
    #     result = point_1 + point_2

    #     # Assert.
    #     self.assertEqual(result, AffinePoint.get_infinity())

#     def test_two_points_with_same_x_and_same_y(self):
#         # Arrange.
#         point_1 = AffinePoint(172235452673, 488838007757)
#         point_2 = AffinePoint(172235452673, 488838007757)

#         # Act.
#         result = point_1 + point_2

#         # Assert.
#         self.assertEqual(result, AffinePoint(215387987039, 765000578277))

#     def test_mix_of_add_and_mul(self):
#         # Arrange.
#         point = AffinePoint(172235452673, 488838007757)

#         # Act.
#         two_mul_point = 2 * point
#         point_add_point = point + point

#         # Assert.
#         self.assertEqual(two_mul_point, AffinePoint(215387987039, 765000578277))
#         self.assertEqual(two_mul_point, point_add_point)

#     def test_mul(self):
#         # Arrange.
#         point = AffinePoint(172235452673, 488838007757)

#         # Act.
#         point_mul_0 = 2 * point
#         point_mul_1 = 2137 * point
#         point_mul_2 = 741274052018 * point
#         point_mul_3 = 649074375334 * point

#         # Assert.
#         self.assertEqual(AffinePoint(215387987039, 765000578277), point_mul_0)
#         self.assertEqual(AffinePoint(464122625441, 361301908555), point_mul_1)
#         self.assertEqual(AffinePoint(702787153408, 513816894152), point_mul_2)
#         self.assertEqual(AffinePoint(748235734737, 753279782927), point_mul_3)

#     def test_add(self):
#         # Arrange.
#         point_1 = AffinePoint(172235452673, 488838007757)
#         point_2 = AffinePoint(748235734737, 753279782927)

#         # Act.
#         point_add_1 = point_1 + point_2
#         point_add_2 = point_1 + point_1

#         # Assert.
#         self.assertEqual(AffinePoint(198482119007, 191241681320), point_add_1)
#         self.assertEqual(AffinePoint(215387987039, 765000578277), point_add_2)


if __name__ == "__main__":
    unittest.main()
