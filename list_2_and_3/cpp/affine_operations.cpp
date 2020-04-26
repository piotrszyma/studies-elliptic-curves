#include <functional>

#include "field.h"

namespace AffineOperations {
  Field::AffinePoint addPoints(Field::AffinePoint first, Field::AffinePoint second) {
    // Implement fields addition.
    return first;
  }
  Field::AffinePoint multiplyByScalar(Field::AffinePoint point, int scalar) {
    // Implement multiply by scalar.

    if (scalar == 2) {
      if (point.isInfinity() || point.y == 0)  {
        return Field::AffinePoint::getInfinity();
      }
    }

    return Field::AffinePoint::getInfinity();
    //     if value == 2:  # TODO: migrate to Fields
    //         if self.is_infinity() or self.y == 0:
    //             return self.get_infinity()

    //         s = ((self.x ** 2) * 3 + self._curve_params.a) * modinv(
    //             2 * self.y, self._curve_params.field_order
    //         )
    //         x2 = (s ** 2) - 2 * self.x
    //         y2 = (s * (self.x - x2)) - self.y

    //         return AffinePoint(x=x2, y=y2)

    //     temp = copy.deepcopy(self)
    //     result = AffinePoint.get_infinity()

    //     while value != 0:
    //         if value & 1 != 0:
    //             result += temp
    //         temp *= 2
    //         value >>= 1

    //     return result
  }
}
