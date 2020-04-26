
class AffinePoint {
  public: 
    FieldNumber x;
    FieldNumber y;

    AffinePoint(FieldNumber x_, FieldNumber y_);
    AffinePoint();

    bool isInfinity();

    static AffinePoint getInfinity();
  
};
