import math
import numbers

class Vec3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z

    def __pos__(self):
        return self

    def __neg__(self):
        return Vec3(-self.x,-self.y,-self.z)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
    def __rmul__(self, other):
        if isinstance(other,numbers.Real):
            return Vec3(other*self.x, other*self.y, other*self.z)
    def __truediv__(self, other):
        if isinstance(other,numbers.Real):
            return Vec3(self.x / other, self.y / other, self.z / other)
        return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def squared_length(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def dot(self,other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self,other):
        return Vec3((self.y*other.z-self.z*other.y),(self.z*other.x-self.x*other.z),(self.x*other.y-self.y*other.x))

    def unit_vector(self):
        return self / self.length()
