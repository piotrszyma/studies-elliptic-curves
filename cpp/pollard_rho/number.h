#ifndef NUMBER_H
#define NUMBER_H

#include <iostream>
#include <gmpxx.h>

class Number {
  private:
    mpz_class value;

  public:
    Number(std::string value_);
    Number(mpz_class value_);

    mpz_class getValue();
    mpz_class getModulus();

    Number operator + (Number anotherNumber);

    Number operator - (Number anotherNumber);

    // Number operator - ();

    Number operator * (Number anotherNumber);

    Number operator / (Number anotherNumber);

    Number operator % (Number anotherNumber);

    bool operator == (Number anotherNumber);

    bool operator != (Number anotherNumber);
};

#endif //NUMBER_H
