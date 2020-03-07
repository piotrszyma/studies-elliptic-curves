#include <iostream>

#include "number.h"
#include "pollard_rho.h"

std::tuple<Number, Point> PollardRho::f(std::tuple<Number, Point> values)
{
  auto [num, point] = values;
  auto [alpha, beta] = point;

  if (num % 3 == 1)
  {
    beta = beta + 1;
    num = (num * y) % p;
  }
  else if (num % 3 == 0)
  {
    alpha = alpha * 2;
    beta = beta * 2;
    num = (num * num) % p;
  }
  else if (num % 3 == 2)
  { // num % 3 == 2
    alpha = alpha + 1;
    num = (g_prim * num) % p;
  }
  else
  {
    throw std::runtime_error("Impossible happend - num % 3 not in [0, 1, 2]?");
  }

  return {num, {alpha, beta}};
}

PollardRho::PollardRho(Number g_prim_, Number p_prim_, Number p_, Number y_) : g_prim(g_prim_), p(p_), p_prim(p_prim_), y(y_){};

Number PollardRho::walk()
{
  Number A{1};
  Number B{1};

  Point poeA{{0}, {0}};
  Point poeB{{0}, {0}};

  int i = 0;

  do
  {
    i++;

    std::tie(A, poeA) = f({A, poeA});
    std::tie(B, poeB) = f(f({B, poeB}));

  } while (A != B);

  auto [alphaA, betaA] = poeA;
  auto [alphaB, betaB] = poeB;

  auto betasInvs = (betaA - betaB).modpow(p_prim - 2, p_prim);
  auto alphasDeltas = alphaB - alphaA;

  return (alphasDeltas * betasInvs) % p_prim;
}

Number PollardRho::run()
{
  return walk();
}
