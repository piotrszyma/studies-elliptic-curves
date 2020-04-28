
MODULUS = None


def set_modulus(modulus):
    global MODULUS 
    MODULUS = modulus


class FieldInt:

    def __init__(self, value):
        
        if MODULUS is None:
            raise RuntimeError('First field.set_modulus(...)')
        
        self.value = value % MODULUS

    def __add__(self, other):
        if isinstance(other, int):
            other = FieldInt(other)
        if not isinstance(other, FieldInt):
            return NotImplemented
        return FieldInt(self.value + other.value)

    def __sub__(self, other):
        if isinstance(other, int):
            other = FieldInt(other)
        if not isinstance(other, FieldInt):
            return NotImplemented
        return FieldInt(self.value - other.value)

    def __neg__(self):
        return FieldInt(-self.value)

    def __mul__(self, other):
        if isinstance(other, int):
            other = FieldInt(other)
        if not isinstance(other, FieldInt):
            return NotImplemented
        return FieldInt(self.value * other.value)

    def __rmul__(self, other):
        return self.__mul__(other)

    def inverse(self):
        if self.value == 0:
            raise ValueError("Division by zero")
        # Extended Euclidean algorithm
        x, y = MODULUS, self.value
        a, b = 0, 1
        while y != 0:
            a, b = b, a - x // y * b
            x, y = y, x % y
        if x == 1:
            return FieldInt(a)
        else:
            raise ValueError("Value and modulus not coprime")

    def __mod__(self, other):
        return self.value % other

    def __pow__(self, other):
        result = pow(self.value, other, MODULUS)
        return FieldInt(result)

    def __eq__(self, other):
        if isinstance(other, int):
            other = FieldInt(other)
        return isinstance(other, FieldInt) and self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    # -- Miscellaneous methods --

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"FieldInt(value={getattr(self, 'value', '???')})"
