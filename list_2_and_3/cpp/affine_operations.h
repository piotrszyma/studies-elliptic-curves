#pragma once

#include <gmpxx.h>

#include "field.h"

namespace AffineOperations {
  Field::AffinePoint addPoints(Field::AffinePoint first, Field::AffinePoint second);
  Field::AffinePoint multiplyByScalar(Field::AffinePoint point, int scalar);
}
