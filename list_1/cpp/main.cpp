/** Pollard rho implemented in cpp

Requires four params passed to stdin, line by line:

- g_prim
- p
- p_prim
- y

passed as integers.

To pass params created from python script, run:
python3 ../py/main.py --genparams --nbits 40 | ./pollard_rho.bin

*/

#include <iostream>

#include <gmpxx.h>

#include "pollard_rho.h"


int main(void)
{
  PollardRho::run_pollard_rho_from_stdin();
  return 0;
}
