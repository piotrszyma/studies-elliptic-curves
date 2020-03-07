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

    Number modpow(Number exp, Number mod);

    Number operator + (Number anotherNumber);
    Number operator + (uint64_t intNumber);
    
    Number operator - (Number anotherNumber);
    Number operator - (int intNumber);

    Number operator * (Number anotherNumber);
    Number operator * (uint64_t intNumber);

    Number operator / (Number anotherNumber);

    Number operator % (Number anotherNumber);
    Number operator % (uint64_t intNumber);

    bool operator == (Number anotherNumber);
    bool operator == (uint64_t intNumber);

    bool operator != (Number anotherNumber);
};

#endif //NUMBER_H
