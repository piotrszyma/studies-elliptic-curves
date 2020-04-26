#include <fstream>
#include <iostream>

#include "utils.h"
#include "field.h"
#include "field_operations.h"
#include "curve_config.h"

namespace CurveUtils {

  // Edward curve def
  // x_2 + y_2 = 1 + d * x_2 * y_2.
  // bool isPointOnCurve(FieldNumber x, FieldNumber y) {
  //   FieldNumber left = x * x + y * y;
  //   FieldNumber right = x.getN(1) + x.getD() * x * x * y * y;
  //   return left == right;
  // }

  int getSeed() {
    unsigned long long int random_value = 0; //Declare value to store data into
    size_t size = sizeof(random_value); //Declare size of data
    std::ifstream urandom("/dev/urandom", std::ios::in|std::ios::binary); //Open stream
    urandom.read(reinterpret_cast<char*>(&random_value), size); //Read from urandom
    return random_value;
  }

  void printPoint(Field::AffinePoint point) {
    std::cout << "X: " << point.x.getValue().get_mpz_t() << std::endl;
    std::cout << "Y: " << point.y.getValue().get_mpz_t() << std::endl << std::endl;
  }


  void assertPointsEqual(Field::AffinePoint expected, Field::AffinePoint actual) {
    assert(expected.x == actual.x);
    assert(expected.y == actual.y);
  }

  Field::AffinePoint getRandomPointOnCurve() {
    gmp_randclass RANDOMNESS (gmp_randinit_default);
    RANDOMNESS.seed(getSeed());
    mpz_class random = RANDOMNESS.get_z_range(Field::FieldNumber::MODULUS);
    Field::AffinePoint basePoint{
      CurveConfig::curveBasePoint.x, 
      CurveConfig::curveBasePoint.y,
    };
    return basePoint * random;
  }
}
