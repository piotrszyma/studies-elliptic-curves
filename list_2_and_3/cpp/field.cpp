#include <iostream>
#include <assert.h>
#include <tuple>

#include "field.h"
#include "field_operations.h"

using namespace Field;

mpz_class FieldNumber::MODULUS;

// TODO: Maybe positiveModulo not needed? Investigate.
FieldNumber::FieldNumber() : value(mpz_class(FieldOperations::positiveModulo(0, FieldNumber::MODULUS))){};
FieldNumber::FieldNumber(mpz_class value_) : value(FieldOperations::positiveModulo(value_, FieldNumber::MODULUS)) {};
FieldNumber::FieldNumber(int value_) : value(mpz_class(FieldOperations::positiveModulo(value_, FieldNumber::MODULUS))) {};

mpz_class FieldNumber::getValue() {
  return value;
}

mpz_class FieldNumber::getModulus() {
  return MODULUS;
}

FieldNumber FieldNumber::operator + (FieldNumber anotherNumber) {
  mpz_class thisValue = getValue();
  mpz_class anotherValue = anotherNumber.getValue();
  mpz_class result;
  mpz_add(result.get_mpz_t(), thisValue.get_mpz_t(), anotherValue.get_mpz_t());
  return FieldNumber(result);
}

FieldNumber FieldNumber::operator - () {
  return FieldNumber(-1) * FieldNumber(this->getValue());
}

FieldNumber FieldNumber::operator - (FieldNumber anotherNumber) {
  mpz_class thisValue = getValue();
  mpz_class anotherValue = anotherNumber.getValue();
  mpz_class result;
  mpz_sub(result.get_mpz_t(), thisValue.get_mpz_t(), anotherValue.get_mpz_t());
  return FieldNumber(result);
}

FieldNumber FieldNumber::operator * (FieldNumber anotherNumber) {
  mpz_class thisValue = getValue();
  mpz_class anotherValue = anotherNumber.getValue();
  mpz_class result;
  mpz_mul(result.get_mpz_t(), thisValue.get_mpz_t(), anotherValue.get_mpz_t());
  return FieldNumber(result);
}

FieldNumber FieldNumber::operator / (FieldNumber anotherNumber) {
  mpz_class result;
  mpz_class modulus_less_two;
  mpz_sub(modulus_less_two.get_mpz_t(), MODULUS.get_mpz_t(), mpz_class(2).get_mpz_t());
  mpz_powm(result.get_mpz_t(), anotherNumber.getValue().get_mpz_t(), modulus_less_two.get_mpz_t(), MODULUS.get_mpz_t());
  return FieldNumber(this->getValue()) * FieldNumber(result);
}

FieldNumber FieldNumber::operator % (FieldNumber anotherNumber) {
  mpz_class result;
  mpz_mod(result.get_mpz_t(), this->getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t());
  return FieldNumber(result);
}

FieldNumber FieldNumber::operator ^ (int number) {
  mpz_class result;
  mpz_class number_(number);
  mpz_powm(result.get_mpz_t(), this->getValue().get_mpz_t(), number_.get_mpz_t(), MODULUS.get_mpz_t());
  return FieldNumber(result);
}

bool FieldNumber::operator == (FieldNumber anotherNumber) {
  return mpz_cmp(getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t()) == 0;
}

bool FieldNumber::operator != (FieldNumber anotherNumber) {
  return mpz_cmp(getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t()) != 0;
}
