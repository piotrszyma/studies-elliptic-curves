#include <iostream>
#include <gmpxx.h>

#define INF AffinePoint{0, 0, 0, true}

mpz_class* FIELD_ORDER;

struct AffinePoint
{
  mpz_class x;
  mpz_class y;
  mpz_class mod;
  bool inf = false;
  
  // addop. doesn't modify object. therefore const.
  AffinePoint operator+(const AffinePoint& other) const
  {
      if (inf) return AffinePoint{other.x, other.y, mod};
      if (other.inf) return AffinePoint{x, y, mod};
      if (x == other.x) {
        if (y == other.y) {
          return AffinePoint{x, y, mod} * 2;
        } else {
          return AffinePoint{0, 0, 0, true};
        }
      }

      return AffinePoint{x + other.x, y + other.y, mod};
  }

  inline bool isInf() {
    return inf;
  }

  // // addop. doesn't modify object. therefore const.
  AffinePoint operator*(const int& other) const
  {
    return AffinePoint{x, y, mod};
  }

};

int main(void) {
  // CurveParams(base_point=CurveBasePoint(x=4301312295, y=6048067141, z=1), a=12047472956, b=15327760553, curve_order=33520574929, field_order=33520808467)
  
  // Initialize base point.
  std::string base_point_x_str = "4301312295";
  std::string base_point_y_str = "6048067141";

  // Initialize field order.
  std::string field_order_str = "33520808467";
  mpz_class field_order(field_order_str, 10);
  FIELD_ORDER = &field_order;

  int k = 7;

  AffinePoint base_point{
    mpz_class(base_point_x_str, 10), 
    mpz_class(base_point_y_str, 10),
    mpz_class(field_order_str, 10),
  };

  AffinePoint mul_point = base_point + base_point;

  // mpz_class g_prim(g_prim_str, 10), p(p_str, 10), p_prim(p_prim_str, 10), y(y_str, 10);

  return 0;
}
