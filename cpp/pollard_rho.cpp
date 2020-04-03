#include <iostream>
#include <gmpxx.h>

namespace PollardRho
{

inline void f(mpz_class *num, mpz_class *alpha, mpz_class *beta, mpz_class *y, mpz_class *p, mpz_class *p_prim, mpz_class *g_prim)
{
  switch (mpz_class res = *num % 3; res.get_ui())
  {
  case 1:
    *beta += 1;
    *beta %= *p_prim;
    *num *= *y;
    *num %= *p;
    break;
  case 0:
    *alpha *= 2;
    *alpha %= *p_prim;
    *beta *= 2;
    *beta %= *p_prim;
    *num *= *num;
    *num %= *p;
    break;
  case 2:
    *alpha += 1;
    *alpha %= *p_prim;
    *num *= *g_prim;
    *num %= *p;
    break;
  default:
    throw std::runtime_error("x % 3 not in [0, 1, 2]?");
  }
}

mpz_class pollard_rho_mpz(mpz_class *g_prim, mpz_class *p, mpz_class *p_prim, mpz_class *y)
{
  mpz_class A(1), B(1), alphaA(0), betaA(0), alphaB(0), betaB(0);

  do
  {
    f(&A, &alphaA, &betaA, y, p, p_prim, g_prim);
    f(&B, &alphaB, &betaB, y, p, p_prim, g_prim);
    f(&B, &alphaB, &betaB, y, p, p_prim, g_prim);
  } while (A != B);

  mpz_class betasInv;
  mpz_class betaDeltas = betaA - betaB;
  mpz_class p_primMinTwo = *p_prim - 2;
  mpz_powm(betasInv.get_mpz_t(), betaDeltas.get_mpz_t(), p_primMinTwo.get_mpz_t(), (*p_prim).get_mpz_t());
  return ((alphaB - alphaA) * betasInv) % *p_prim;
}

void run_pollard_rho_from_stdin()
{
  std::string g_prim_str, p_str, p_prim_str, y_str;
  std::cin >> g_prim_str;
  std::cin >> p_str;
  std::cin >> p_prim_str;
  std::cin >> y_str;

  std::cout << "Running for "
            << "g_prim: " << g_prim_str << " "
            << "p: " << p_str << " "
            << "p_prim: " << p_prim_str << " "
            << "y: " << y_str << std::endl;

  mpz_class g_prim(g_prim_str, 10), p(p_str, 10), p_prim(p_prim_str, 10), y(y_str, 10);
  mpz_class x_found = pollard_rho_mpz(&g_prim, &p, &p_prim, &y);

  std::cout << "x_found: " << x_found << std::endl;

  mpz_class result;
  mpz_powm(result.get_mpz_t(), g_prim.get_mpz_t(), x_found.get_mpz_t(), p.get_mpz_t());
  std::cout << "g_prim ^ x_found: " << result << std::endl;

  std::cout << "y: " << y << std::endl;
}

} // namespace PollardRho
