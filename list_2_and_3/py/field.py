import random

import shared


MODULUS = None
INVERSE_CACHE = {}


def set_modulus(modulus):
    global MODULUS
    MODULUS = modulus


class FieldInt:
    _instances = {}

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

    def __float__(self):
        return float(self.value)

    def __and__(self, other):
        return self.value & other
        
    def __rshift__(self, other):
        self.value >>= other

    @classmethod
    def random(cls, min_value=0, max_value=1):
        return cls(random.randint(min_value, max_value))

    def inverse(self):
        if self.value in INVERSE_CACHE:
            return INVERSE_CACHE[self.value]

        if self.value == 0:
            raise ValueError("Division by zero")

        INVERSE_CACHE[self.value] = FieldInt(shared.modinv(self.value, MODULUS))

        return INVERSE_CACHE[self.value]

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
