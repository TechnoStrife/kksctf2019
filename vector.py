import operator
from typing import overload, Union, Tuple, List, Any, Optional

import math

__all__ = [
    'Vector'
]

Number = Union[int, float]
VectorLike = Union[
    None,
    'Vector',
    Number,
    Tuple[Number, Number]
]


def is_number(x: Any) -> bool:
    return isinstance(x, (int, float))


def _reflect(operation):
    def reflected(self, other):
        return operation(_convert_other(other), self)

    return reflected


# noinspection PyAttributeOutsideInit
class Vector:
    @overload
    def __init__(self):
        """
        >>> Vector()
        <Vector 0, 0>
        """

    @overload
    def __init__(self, xy: Number):
        """
        Both x and y = xy
        :param xy: int or float

        >>> Vector(5)
        <Vector 5, 5>
        """

    @overload
    def __init__(self, x: Number, y: Number):
        """
        :param x: int or float
        :param y: int or float

        >>> Vector(3.5, 4.8)
        <Vector 3.5, 4.8>
        >>> Vector(x=1, y=2)
        <Vector 1, 2>
        """

    @overload
    def __init__(self, vec: 'Vector'):
        """
        :param vec: Vector

        >>> Vector(Vector(1, 1))
        <Vector 1, 1>
        """

    @overload
    def __init__(self, xy: Union[Tuple[Number, Number], List[Number]]):
        """
        :param xy: Iterable[Number, Number]
        x = xy[0]
        y = xy[1]

        >>> Vector([3, 4])
        <Vector 3, 4>
        >>> Vector((3, 4))
        <Vector 3, 4>
        """

    def __init__(self, x=None, y=None):
        if x is None and y is None:
            self.x = 0
            self.y = 0
        elif x is not None and y is None:
            arg = x
            if isinstance(x, Vector):
                self.x = arg.x
                self.y = arg.y
            elif is_number(arg):
                self.x = arg
                self.y = arg
            elif isinstance(arg, (tuple, list)) and len(arg) == 2:
                self.x, self.y = arg
            else:
                raise TypeError('incorrect parameter')
        elif is_number(x) and is_number(y):
            self.x = x
            self.y = y
        else:
            raise TypeError('incorrect parameters')

    def copy(self) -> 'Vector':
        """
        Copies this vector and returns it
        :return: copy of the vector

        >>> v = Vector(1, 2)
        >>> v2 = v.copy()
        >>> v == v2
        True
        >>> v is v2
        False
        """
        return Vector(self.x, self.y)

    @property
    def coords(self) -> Tuple[int, int]:
        """
        Returns tuple of integral x and y
        :return: int(x), int(y)

        >>> Vector(3.5, 4.8).coords
        (3, 4)
        """
        return int(self.x), int(self.y)

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __repr__(self):
        return '<Vector %s, %s>' % (self.x, self.y)

    def __add__(self, other: VectorLike) -> 'Vector':
        """
        Sums self.x + other.x, self.y + other.y
        :param other: Vector-like object
        :return: Vector

        >>> Vector(1, 5) + 2.5
        <Vector 3.5, 7.5>
        >>> Vector(5, 5) + Vector(2, -2)
        <Vector 7, 3>
        >>> Vector(5, 5) + (2, 3)
        <Vector 7, 8>
        """
        other = _convert_other(other)
        return Vector(self.x + other.x, self.y + other.y)

    __radd__ = __add__

    def __iadd__(self, other: VectorLike) -> 'Vector':
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: VectorLike) -> 'Vector':
        """
        Subs self.x - other.x, self.y - other.y
        :param other: Vector-like object
        :return: Vector

        >>> Vector(1, 5) - 2.5
        <Vector -1.5, 2.5>
        >>> Vector(5, 5) - Vector(2, -2)
        <Vector 3, 7>
        >>> Vector(5, 5) - (2, 3)
        <Vector 3, 2>
        """
        other = _convert_other(other)
        return Vector(self.x - other.x, self.y - other.y)

    __rsub__ = _reflect(operator.sub)

    def __isub__(self, other: VectorLike) -> 'Vector':
        other = _convert_other(other)
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: VectorLike) -> 'Vector':
        """
        Multiplies x and y separately
        Returns self.x * other.x, self.y * other.y
        :param other: Vector-like object
        :return: Vector

        >>> Vector(1, 5) * 2.5
        <Vector 2.5, 12.5>
        >>> Vector(5, 5) * Vector(2, -2)
        <Vector 10, -10>
        >>> Vector(5, 5) * (2, 3)
        <Vector 10, 15>
        """
        other = _convert_other(other)
        return Vector(self.x * other.x, self.y * other.y)

    __rmul__ = __mul__

    def __imul__(self, other: VectorLike) -> 'Vector':
        other = _convert_other(other)
        self.x *= other.x
        self.y *= other.y
        return self

    def __truediv__(self, other: VectorLike) -> 'Vector':
        """
        Divides x and y separately
        Returns self.x / other.x, self.y / other.y
        :param other: Vector-like object
        :return: Vector

        >>> Vector(1, 5) / 2.5
        <Vector 0.4, 2.0>
        >>> Vector(5, 5) / Vector(2, -2)
        <Vector 2.5, -2.5>
        >>> Vector(5, 6) / (2, 3)
        <Vector 2.5, 2.0>
        """
        other = _convert_other(other)
        return Vector(self.x / other.x, self.y / other.y)

    __rtruediv__ = _reflect(operator.truediv)

    def __idiv__(self, other: VectorLike) -> 'Vector':
        other = _convert_other(other)
        self.x /= other.x
        self.y /= other.y
        return self

    __div__ = __truediv__
    __rdiv__ = __rtruediv__

    def __floordiv__(self, other):
        """
        Divides x and y separately with cutting to int
        Returns self.x / other.x, self.y / other.y
        :param other: Vector-like object
        :return: Vector

        >>> Vector(10, 11) // 2
        <Vector 5, 5>
        >>> Vector(5, 7) // Vector(2, 4)
        <Vector 2, 1>
        >>> Vector(5, 7) // (2, 4)
        <Vector 2, 1>
        """
        other = _convert_other(other)
        return Vector(self.x // other.x, self.y // other.y)

    __rfloordiv__ = _reflect(operator.floordiv)

    def __ifloordiv__(self, other: VectorLike) -> 'Vector':
        other = _convert_other(other)
        self.x //= other.x
        self.y //= other.y
        return self

    def __mod__(self, other: VectorLike) -> 'Vector':
        """
        Returns self.x % other.x, self.y % other.y
        :param other: Vector-like object
        :return: Vector

        >>> Vector(1, 5) % 2.5
        <Vector 1.0, 0.0>
        >>> Vector(5, 5) % Vector(2, -2)
        <Vector 1, -1>
        >>> Vector(5, 5) % (2, 3)
        <Vector 1, 2>
        """
        other = _convert_other(other)
        return Vector(self.x % other.x, self.y % other.y)

    __rmod__ = _reflect(operator.mod)

    def __float__(self) -> float:
        """
        Returns hypotenuse of the vector
        :return: math.hypot(x, y)

        >>> float(Vector(3, 4))
        5.0
        >>> float(Vector(5, 5))
        7.0710678118654755
        """
        return math.hypot(self.x, self.y)

    def __int__(self) -> int:
        """
        Returns integral hypotenuse of the vector
        :return: int(math.hypot(x, y))

        >>> int(Vector(3, 4))
        5
        >>> int(Vector(5, 5))
        7
        """
        return int(self.__float__())

    hypot = __float__
    __abs__ = __float__

    def sum_xy(self) -> Number:
        """
        Returns sum of x and y
        :return: float or int
        """

    def normalize(self) -> None:
        """
        Makes vector length = 1 and pointing in the same direction
        :return: Vector
        """
        self_len = self.len
        self.x /= self_len
        self.y /= self_len

    def normalized(self) -> 'Vector':
        """
        Returns vector pointing in the same direction with length 1
        :return: Vector
        """
        return self / self.len

    def to_math_coords(self) -> 'Vector':
        """
        Returns vector with -y because displays count y downwards
        :return: Vector
        """
        return Vector(self.x, -self.y)

    def to_display_coords(self) -> 'Vector':
        """
        Returns vector with -y because displays count y downwards
        :return: Vector
        """
        return Vector(self.x, -self.y)

    def quarter(self) -> int:
        """

        :return: quarter where vector is pointing

        >>> Vector(1, 1).quarter()
        1
        >>> Vector(-1, 1).quarter()
        2
        >>> Vector(-1, -1).quarter()
        3
        >>> Vector(1, -1).quarter()
        4

        Vectors with x or y = 0 don't have quarers
        >>> Vector(0, 1).quarter()
        0
        """
        if self.x == 0 or self.y == 0:
            return 0
        return ((self.y <= 0) << 1) + ((self.x > 0) ^ (self.y > 0)) + 1

    @property
    def len(self) -> float:
        """
        Returns hypotenuse of the vector. Same as math.hypot(x, y)
        :return: float

        >>> Vector(3, 4).len
        5.0
        >>> Vector(5, 5).len
        7.0710678118654755
        """
        return self.__float__()

    @property
    def tan(self) -> float:
        """
        :return: math.tan(vector.angle)

        >>> Vector(3, 4).tan
        1.3333333333333333
        >>> Vector(-3, -4).tan
        1.3333333333333333
        >>> Vector(1, 0).tan
        0
        >>> Vector(-1, 0).tan
        0
        >>> Vector(0, 1).tan
        inf
        >>> Vector(0, -1).tan
        -inf
        """
        if self.x == 0 and self.y == 0:
            raise ValueError('zero-vector has no tangent')
        if self.x == 0:
            return math.inf if self.y > 0 else -math.inf
        if self.y == 0:
            return 0
        return self.y / self.x

    @property
    def angle(self) -> float:
        """
        Returns angle where vector is pointing in radians
        :return: float

        >>> Vector(3, 4).angle
        0.9272952180016122
        >>> Vector(1, 0).angle
        0.0
        """
        if self.x == 0:
            if self.y == 0:
                raise ValueError('zero-vector has no angle')
            return math.pi / 2 if self.y > 0 else math.pi * 3 / 2
        if self.y == 0:
            return 0.0 if self.x > 0 else math.pi
        angle = math.atan(self.y / self.x)
        quarter = self.quarter()
        if quarter == 2:  # angle is in 4 quarter
            angle = math.pi / 2 - angle
        elif quarter == 3:
            angle = -math.pi / 2 - angle
        return angle

    @angle.setter
    def angle(self, radians: Number):
        """
        :param radians: angle where you want vector to be pointing in radians
        :return: None
        See Vector.angle_deg for examples
        """
        radians -= self.angle
        sin_t = math.sin(radians)
        cos_t = math.cos(radians)
        x = self.x
        y = self.y
        self.x = x * cos_t - y * sin_t
        self.y = x * sin_t + y * cos_t

    @property
    def angle_deg(self) -> float:
        """
        Returns angle where vector is pointing in degrees. Same as math.degrees(self.angle)
        :return: float

        >>> Vector(3, 4).angle_deg
        53.13010235415598
        >>> Vector(1, 0).angle_deg
        0.0
        >>> Vector(-1, 0).angle_deg
        180.0
        >>> Vector(0, 1).angle_deg
        90.0
        >>> Vector(0, -1).angle_deg
        270.0
        >>> Vector(1, 1).angle_deg
        45.0
        >>> Vector(-1, 1).angle_deg
        135.0
        >>> Vector(-1, -1).angle_deg
        225.0
        >>> Vector(1, -1).angle_deg
        315.0
        """
        return math.degrees(self.angle)

    @angle_deg.setter
    def angle_deg(self, alpha: Number):
        """
        :param alpha: angle where you want vector to be pointing in degrees
        :return: None

        >>> v = Vector(1, 0)
        >>> v.angle_deg = 180
        >>> v
        <Vector -1.0, 0.0>
        180.0
        >>> v.angle_deg = 90
        >>> v
        <Vector 0.0, 1.0>
        >>> v.angle_deg = 270
        >>> v
        <Vector 0.0, -1.0>
        >>> v.angle_deg = 45
        >>> v
        <Vector 1.0, 1.0>
        >>> v.angle_deg = 135
        >>> v
        <Vector -1.0, 1.0>
        >>> v.angle_deg = 225
        >>> v
        <Vector -1.0, -1.0>
        >>> v = Vector(1, 0).angle_deg
        >>> v.angle_deg = 53.13010235415598
        <Vector 3.0, 4.0>
        """
        self.angle = math.radians(alpha)

    def rotate(self, radians: Optional[Number] = None, degrees: Optional[Number] = None):
        """
        Returns copy of the vector with corresponding angle
        If only alpha is passed, t = math.radians(alpha)
        If both are passed t will be used
        :param radians: number, angle in radians
        :param degrees: number, angle
        :return: Vector

        >>> Vector(1, 1).rotate(degrees=135.0)
        <Vector -0.9999999999999999, 1.0>
        """
        if radians is None and degrees is None:
            raise ValueError('you have to pass t or alpha')
        if radians is None and degrees is not None:
            radians = math.radians(degrees)
        vec = self.copy()
        vec.angle = radians
        return vec

    def __pos__(self) -> 'Vector':
        """
        Does nothing
        :return: Vector
        """
        return self

    def __neg__(self) -> 'Vector':
        """
        Returns copy of the vector with x and y both negated
        :return: Vector

        >>> -Vector(1, 1)
        <Vector -1, -1>
        """
        return Vector(-self.x, -self.y)

    def __round__(self, prescision=None) -> 'Vector':
        """
        Returns copy of the vector with x and y both rounded
        :return: Vector

        >>> round(Vector(2**0.5, 3**0.5), 2)
        <Vector 1.41, 1.73>
        """
        return Vector(round(self.x, prescision), round(self.y, prescision))

    def __floor__(self) -> 'Vector':
        """
        Returns copy of the vector with x and y both floor-rounded
        :return: Vector

        >>> math.floor(Vector(2**0.5, 3**0.5))
        <Vector 1, 1>
        """
        return Vector(math.floor(self.x), math.floor(self.y))

    def __ceil__(self) -> 'Vector':
        """
        Returns copy of the vector with x and y both ceil-rounded
        :return: Vector

        >>> math.ceil(Vector(2**0.5, 3**0.5))
        <Vector 2, 2>
        """
        return Vector(math.ceil(self.x), math.ceil(self.y))

    def __trunc__(self) -> 'Vector':
        """
        Returns copy of the vector with x and y both trunceted
        :return: Vector

        >>> math.trunc(Vector(2**0.5, 3**0.5))
        <Vector 1, 1>
        """
        return Vector(math.trunc(self.x), math.trunc(self.y))

    def __eq__(self, other) -> bool:
        """
        Returns true if both x and y in both vectors are equal
        :return: bool

        >>> Vector(1, 1) == Vector(1, 1.0)
        True
        >>> Vector(1.1, 1) == Vector(1, 1)
        False
        """
        other = _convert_other(other)
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        """
        Returns true if x or y in vectors are not equal
        :return: bool

        >>> Vector(1, 1) != Vector(1, 1.0)
        False
        >>> Vector(1.1, 1) != Vector(1, 1)
        True
        """
        return not self == other

    def __len__(self):
        """
        :return: 2

        >>> len(Vector())
        2
        """
        return 2  # len([self.x, self.y])

    def __iter__(self):
        """
        Iterates over x and y

        >>> list(Vector())
        [0, 0]
        """
        yield self.x
        yield self.y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        raise IndexError('Vector has only 2 items')

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError('Vector has only 2 items')


def _convert_other(other: VectorLike) -> 'Vector':
    if isinstance(other, Vector):
        return other
    if is_number(other):
        return Vector(other, other)
    if isinstance(other, (list, tuple)):
        if len(other) == 2 and is_number(other[0]) and is_number(other[1]):
            return Vector(other[0], other[1])
    raise NotImplementedError("Can't convert type %s to Vector" % type(other))
