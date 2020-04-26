#pragma once

#include <gmpxx.h>

namespace Field {

class FieldNumber {
  private:
    mpz_class value;

  public:
    static mpz_class MODULUS;

    FieldNumber();
    FieldNumber(mpz_class value_);
    FieldNumber(int value_);

    mpz_class getValue();
    mpz_class getModulus();

    FieldNumber operator + (FieldNumber anotherNumber);

    FieldNumber operator - ();
    
    FieldNumber operator - (FieldNumber anotherNumber);

    FieldNumber operator * (FieldNumber anotherNumber);

    FieldNumber operator / (FieldNumber anotherNumber);

    FieldNumber operator % (FieldNumber anotherNumber);

    FieldNumber operator ^ (int number);

    bool operator == (FieldNumber anotherNumber);

    bool operator != (FieldNumber anotherNumber);
};
}
