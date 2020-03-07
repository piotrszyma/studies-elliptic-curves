#include "number.h"


Number::Number(const std::string value_)
{
  mpz_init_set_str(this->value.get_mpz_t(), value_.c_str(), 10);
}
Number::Number(mpz_class value_) : value(value_){};

mpz_class Number::getValue()
{
  return value;
}

Number Number::operator+(Number anotherNumber)
{
  mpz_class result;
  mpz_add(result.get_mpz_t(), this->getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t());
  return Number(result);
}

Number Number::operator-(Number anotherNumber)
{
  mpz_class result;
  mpz_sub(result.get_mpz_t(), this->getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t());
  return Number(result);
}

Number Number::operator*(Number anotherNumber)
{
  mpz_class result;
  mpz_mul(result.get_mpz_t(), this->getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t());
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
  mpz_mod(result.get_mpz_t(), this->getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t());
  return Number(result);
}

bool Number::operator==(Number anotherNumber)
{
  return mpz_cmp(getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t()) == 0;
}

bool Number::operator!=(Number anotherNumber)
{
  return mpz_cmp(getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t()) != 0;
}
