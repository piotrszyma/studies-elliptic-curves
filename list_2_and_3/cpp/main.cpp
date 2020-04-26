#include <iostream>
#include <tuple>
#include <functional>
#include <assert.h>
#include <utility>

#include <gmpxx.h>

#include "curve_config.h"
#include "field.h"
#include "field_operations.h"
#include "affine_operations.h"
#include "utils.h"

// x_2 + y_2 = 1 + d * x_2 * y_2.
mpz_class MODULUS;
mpz_class A_VALUE;
mpz_class B_VALUE;


int main(void) {
  FieldOperations::setFieldNumberModulusFromStr("33520808467");
  CurveConfig::setCurveParamA("12047472956");
  CurveConfig::setCurveParamB("15327760553");
  CurveConfig::setCurveOrder("33520574929");
  CurveConfig::setCurveBasePoint("4301312295", "6048067141", "1");

  Field::AffinePoint p1 = CurveUtils::getRandomPointOnCurve();

  return 0;
};
