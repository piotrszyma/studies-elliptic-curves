#pragma once

#include "field.h"

namespace CurveUtils {
  // bool isPointOnCurve(Field::FieldNumber x, Field::FieldNumber y);
  // int getSeed();
  void printPoint(Field::AffinePoint point);
  void assertPointsEqual(Field::AffinePoint expected, Field::AffinePoint actual);
  Field::AffinePoint getRandomPointOnCurve();
}
