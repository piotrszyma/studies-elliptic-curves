#pragma once

#include <iostream>
#include <gmpxx.h>

#include "field.h"

namespace FieldOperations {
  void setFieldNumberModulusFromStr(std::string modulus);
  mpz_class positiveModulo(mpz_class value, mpz_class modulus);
  mpz_class expmod(mpz_class b, mpz_class e, mpz_class m);
  mpz_class inverse(mpz_class value, mpz_class modulus);
}
