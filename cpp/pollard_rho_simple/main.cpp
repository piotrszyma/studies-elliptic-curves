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

#include <gmpxx.h>

#include "pollard_rho_simple.h"


void testPollardRhoMpz()
{
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

  mpz_class x_found = pollard_rho_mpz(g_prim, p, p_prim, y);
  
  std::cout << "x_found: " << x_found << std::endl;

  mpz_class result;
  mpz_powm(result.get_mpz_t(), g_prim.get_mpz_t(), x_found.get_mpz_t(), p.get_mpz_t());
  std::cout << "g_prim ^ x_found: " << result << std::endl;

  std::cout << "y: " << y << std::endl;
}

int main(void)
{
  // testPollardRho();
  testPollardRhoMpz();
  return 0;
}
