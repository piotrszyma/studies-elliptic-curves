#pragma once

#include <gmpxx.h>

namespace CurveConfig {
  struct CurveBasePoint {
    mpz_class x;
    mpz_class y;
    mpz_class z;
  };

  CurveBasePoint static curveBasePoint;

  mpz_class static curveParamA;
  mpz_class static curveParamB;
  mpz_class static curveOrder;
  void setCurveParamA(std::string value);
  void setCurveParamB(std::string value);
  void setCurveOrder(std::string value);
  void setCurveBasePoint(std::string x, std::string y, std::string z);
}
