#ifndef POLLARD_RHO_H
#define POLLARD_RHO_H

#include "number.h"

typedef std::tuple<Number, Number> Point;

class PollardRho {
  private:
    Number g_prim;
    Number p;
    Number p_prim;
    Number y;

    Number walk();
    inline void f(Number* value, Number* alpha, Number *beta);

  public:
    PollardRho(Number g_prim_, Number p_prim_, Number p_, Number y_);
    Number run();
};

#endif //POLLARD_RHO_H
