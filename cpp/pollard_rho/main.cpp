/**Pollard rho implemented in cpp

Requires four params passed to stdin, line by line:

- g_prim
- p
- p_prim
- y

passed as integers.

To pass params created from python script, run:
python3 ../../py/main.py --genparams --nbits 40 40 | ./pollard_rho

*/

#include <iostream>

#include "number.h"
#include "pollard_rho.h"

void testPollardRho()
{
  std::string g_prim_str;
  std::cin >> g_prim_str;
  std::string p_str;
  std::cin >> p_str;
  std::string p_prim_str;
  std::cin >> p_prim_str;
  std::string y_str;
  std::cin >> y_str;

  Number g_prim{g_prim_str};
  Number p{p_str};
  Number p_prim{p_prim_str};
  Number y{y_str};

  std::cout << "Running for "
            << "g_prim: " << g_prim_str << " "
            << "p: " << p_str << " "
            << "p_prim: " << p_prim_str << " "
            << "y: " << y_str << std::endl;

  PollardRho instance{g_prim, p_prim, p, y};

  Number x = instance.run();

  std::cout << "x_found: " << x.getValue() << std::endl;
  std::cout << "g_prim ^ x_found: " << g_prim.modpow(x, p).getValue() << std::endl;
  std::cout << "y: " << y.getValue() << std::endl;
}

int main(void)
{
  testPollardRho();
  return 0;
}
