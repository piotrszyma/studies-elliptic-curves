#include <iostream>

#include "number.h"
#include "pollard_rho.h"

void testPollardRho() {
  Number g_prim { "356322593039" };
  Number p { "554023630907" };
  Number p_prim { "277011815453" };
  Number y { "357059504410" };

  PollardRho instance { g_prim, p_prim, p, y };
  Number x = instance.run();

  std::cout << x.getValue() << std::endl;
}

void testNumber() {
  Number a {"8"};
  // Number b {"3"};
  Number c = a % 3;
  std::cout << c.getValue() << std::endl;
}

int main(void) {
  // testNumber(); 
  testPollardRho();
  return 0;
}
