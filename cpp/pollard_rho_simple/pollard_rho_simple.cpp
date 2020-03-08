#include <iostream>
#include <gmpxx.h>

inline void f(mpz_class *num, mpz_class *alpha, mpz_class *beta, mpz_class *y, mpz_class *p, mpz_class *g_prim)
{
  mpz_class res = *num % 3;

  switch (res.get_ui())
  {
  case 1:
    *beta = *beta + 1;
    *num = (*num * *y) % *p;
    break;
  case 0:
    *alpha = *alpha * 2;
    *beta = *beta * 2;
    *num = (*num * *num) % *p;
    break;
  case 2:
    *alpha = *alpha + 1;
    *num = (*g_prim * *num) % *p;
    break;
  default:
    throw std::runtime_error("x % 3 not in [0, 1, 2]?");
  }
}

mpz_class pollard_rho_mpz(mpz_class *g_prim, mpz_class *p, mpz_class *p_prim, mpz_class *y)
{
  mpz_class A(1);
  mpz_class B(1);
  mpz_class alphaA(0);
  mpz_class betaA(0);
  mpz_class alphaB(0);
  mpz_class betaB(0);

  do
  {
    f(&A, &alphaA, &betaA, y, p, g_prim);
    f(&B, &alphaB, &betaB, y, p, g_prim);
    f(&B, &alphaB, &betaB, y, p, g_prim);
  } while (A != B);

  mpz_class betasInv;
  mpz_class betaDeltas;
  betaDeltas = betaA - betaB;
  mpz_class p_primMinTwo = *p_prim - 2;
  mpz_powm(betasInv.get_mpz_t(), betaDeltas.get_mpz_t(), p_primMinTwo.get_mpz_t(), (*p_prim).get_mpz_t());
  return ((alphaB - alphaA) * betasInv) % *p_prim;
}
