#include <iostream>
#include <gmpxx.h>

namespace PollardRho
{

inline void f(mpz_class *num, mpz_class *alpha, mpz_class *beta, mpz_class *y, mpz_class *p, mpz_class *g_prim)
{
  switch (mpz_class res = *num % 3; res.get_ui())
  {
  case 1:
    *beta += 1;
    *num *= *y;
    *num %= *p;
    break;
  case 0:
    *alpha *= 2;
    *beta *= 2;
    *num *= *num;
    *num %= *p;
    break;
  case 2:
    *alpha += 1;
    *num *= *g_prim;
    *num %= *p;
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

void run_pollard_rho_from_stdin() {
  std::string g_prim_str;
  std::cin >> g_prim_str;
  std::string p_str;
  std::cin >> p_str;
  std::string p_prim_str;
  std::cin >> p_prim_str;
  std::string y_str;
  std::cin >> y_str;

  std::cout << "Running for "
            << "g_prim: " << g_prim_str << " "
            << "p: " << p_str << " "
            << "p_prim: " << p_prim_str << " "
            << "y: " << y_str << std::endl;

  mpz_class g_prim(g_prim_str, 10);
  mpz_class p(p_str, 10);
  mpz_class p_prim(p_prim_str, 10);
  mpz_class y(y_str, 10);

  mpz_class x_found = pollard_rho_mpz(&g_prim, &p, &p_prim, &y);
  
  std::cout << "x_found: " << x_found << std::endl;

  mpz_class result;
  mpz_powm(result.get_mpz_t(), g_prim.get_mpz_t(), x_found.get_mpz_t(), p.get_mpz_t());
  std::cout << "g_prim ^ x_found: " << result << std::endl;

  std::cout << "y: " << y << std::endl;
}

} // namespace PollardRho
