#include <iostream>
#include "number.h"

Number::Number(const std::string value_)
{
  mpz_init_set_str(this->value.get_mpz_t(), value_.c_str(), 10);
}

Number::Number(const uint64_t value_)
{
  mpz_init_set_ui(this->value.get_mpz_t(), value_);
}
Number::Number(mpz_class value_) : value(value_){};

mpz_class Number::getValue()
{
  return value;
}

Number Number::modpow(Number exp, Number mod) {
  // Assuming p is prime
  mpz_class result;
  mpz_powm(result.get_mpz_t(), getValue().get_mpz_t(), exp.getValue().get_mpz_t(), mod.getValue().get_mpz_t());
  return Number(result);
}

Number Number::operator+(Number anotherNumber)
{
  mpz_class result;
  mpz_add(result.get_mpz_t(), this->getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t());
  return Number(result);
}

Number Number::operator+(uint64_t intNumber)
{
  mpz_class result;
  mpz_add_ui(result.get_mpz_t(), this->getValue().get_mpz_t(), intNumber);
  return Number(result);
}

Number Number::operator-(Number anotherNumber)
{
  mpz_class result;
  mpz_sub(result.get_mpz_t(), this->getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t());
  return Number(result);
}
Number Number::operator-(int intNumber)
{
  mpz_class result;
  mpz_sub_ui(result.get_mpz_t(), this->getValue().get_mpz_t(), intNumber);
  return Number(result);
}

Number Number::operator*(Number anotherNumber)
{
  mpz_class result;
  mpz_mul(result.get_mpz_t(), this->getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t());
  return Number(result);
}

Number Number::operator*(uint64_t intNumber)
{
  mpz_class result;
  mpz_mul_ui(result.get_mpz_t(), this->getValue().get_mpz_t(), intNumber);
  return Number(result);
}

Number Number::operator/(Number anotherNumber)
{
  mpz_class result;
  mpz_div(result.get_mpz_t(), this->getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t());
  return Number(result);
}

Number Number::operator%(Number anotherNumber)
{
  mpz_class result;
  mpz_mod(result.get_mpz_t(), getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t());
  return Number(result);
}
Number Number::operator%(uint64_t intNumber)
{
  mpz_class result;
  mpz_mod_ui(result.get_mpz_t(), this->getValue().get_mpz_t(), intNumber);
  return Number(result);
}

bool Number::operator==(Number anotherNumber)
{
  return mpz_cmp(getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t()) == 0;
}

bool Number::operator==(uint64_t intNumber)
{
  return mpz_cmp_ui(getValue().get_mpz_t(), intNumber) == 0;
}

bool Number::operator!=(Number anotherNumber)
{
  return mpz_cmp(getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t()) != 0;
}
