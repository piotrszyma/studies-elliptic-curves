#include <gmpxx.h>

#include "field.h"

namespace FieldOperations {
  // TODO: Move to field setup?
  void setFieldNumberModulusFromStr(std::string modulus) {
    Field::FieldNumber::MODULUS = mpz_class(modulus, 10);
  }

  mpz_class positiveModulo(mpz_class value, mpz_class modulus) {
    mpz_class result;
    mpz_mod(result.get_mpz_t(), value.get_mpz_t(), modulus.get_mpz_t());
    return result;
    // return (value % modulus + modulus) % modulus;
  }

  mpz_class expmod(mpz_class b, mpz_class e, mpz_class m) {
    mpz_class result;
    mpz_powm(result.get_mpz_t(), b.get_mpz_t(), e.get_mpz_t(), m.get_mpz_t());
    return result;
  }

  mpz_class inverse(mpz_class value, mpz_class modulus) {
    mpz_class result;
    mpz_invert(result.get_mpz_t(), value.get_mpz_t(), modulus.get_mpz_t());
    return result;
  }
}
