import shared


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
        return FieldInt(shared.modinv(self.value, MODULUS))

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
