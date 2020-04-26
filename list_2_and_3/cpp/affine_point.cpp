
class AffinePoint {
  public: 
    FieldNumber x;
    FieldNumber y;

    AffinePoint(FieldNumber x_, FieldNumber y_) : x(x_), y(y_) {};
    AffinePoint() {
      x = NULL;
      y = NULL;
    }

    bool isInfinity() {
      return x == NULL;
    }

    static AffinePoint getInfinity() {
      return AffinePoint();
    }
  
};
