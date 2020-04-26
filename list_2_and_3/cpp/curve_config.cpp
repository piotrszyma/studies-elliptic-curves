#include <iostream>
#include <gmpxx.h>

#include "curve_config.h"

namespace CurveConfig {
  void setCurveParamA(std::string value) {
    curveParamA = mpz_class(value, 10);
  }

  void setCurveParamB(std::string value) {
    curveParamB = mpz_class(value, 10);
  }

  void setCurveOrder(std::string value) {
    curveOrder = mpz_class(value, 10);
  }

  void setCurveBasePoint(std::string x, std::string y, std::string z) {
    curveBasePoint = CurveBasePoint{
      mpz_class(x, 10), 
      mpz_class(y, 10), 
      mpz_class(z, 10), 
    };
  }
}
