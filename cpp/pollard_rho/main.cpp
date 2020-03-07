#include <iostream>

#include "number.h"
#include "pollard_rho.h"

int main(void) {
  Number g_prim { "356322593039" };
  Number p { "554023630907" };
  Number p_prim { "277011815453" };
  Number y { "357059504410" };

  PollardRho instance { g_prim, p_prim, p, y };
  Number x = instance.run();

  std::cout << x.getValue() << std::endl;

  return 0;
}
