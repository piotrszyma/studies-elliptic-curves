#include <iostream>

#include "number.h"
#include "pollard_rho.h"
void PollardRho::f(Number* value, Number* alpha, Number *beta)
{

  Number res = *value % 3;

  if (res == 1)
  {
    *beta = *beta + 1;
    *value = (*value * y) % p;
  }
  else if (res == 0)
  {
    *alpha = *alpha * 2;
    *beta = *beta * 2;
    *value = (*value * *value) % p;
  }
  else if (res == 2)
  { // num % 3 == 2
    *alpha = *alpha + 1;
    *value = (g_prim * *value) % p;
  }
  else
  {
    throw std::runtime_error("Impossible happend - num % 3 not in [0, 1, 2]?");
  }
}

PollardRho::PollardRho(Number g_prim_, Number p_prim_, Number p_, Number y_) : g_prim(g_prim_), p(p_), p_prim(p_prim_), y(y_){};

Number PollardRho::walk()
{
  Number A{1};
  Number B{1};

  Number alphaA{0};
  Number betaA{0};
  Number alphaB{0};
  Number betaB{0};

  do
  {
    f(&A, &alphaA, &betaA);
    f(&B, &alphaB, &betaB);
    f(&B, &alphaB, &betaB);
  } while (A != B);


  auto betasInvs = (betaA - betaB).modpow(p_prim - 2, p_prim);
  auto alphasDeltas = alphaB - alphaA;

  return (alphasDeltas * betasInvs) % p_prim;
}

Number PollardRho::run()
{
  return walk();
}
