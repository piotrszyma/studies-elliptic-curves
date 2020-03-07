#ifndef POLLARD_RHO_H
#define POLLARD_RHO_H

#include "number.h"

class PollardRho {
  private:
    Number g_prim;
    Number p;
    Number p_prim;
    Number y;

    Number walk();

  public:
    PollardRho(Number g_prim_, Number p_prim_, Number p_, Number y_);

    Number run();
};

#endif //POLLARD_RHO_H
