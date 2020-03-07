#include "number.h"
#include "pollard_rho.h"

PollardRho::PollardRho(Number g_prim_, Number p_prim_, Number p_, Number y_) : g_prim(g_prim_), p(p_), p_prim(p_prim_), y(y_){};

Number PollardRho::walk()
{

  // Number A(p.getValue().get_mpz_t(), p.getModulus().get_mpz_t());
  // Number p_prim("277011815453", "554023630907");
  Number x("1");
  return x;
}

Number PollardRho::run() {
  Number x { "1" };
  return x;
}
