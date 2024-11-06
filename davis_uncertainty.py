import numpy as np

class Quantity:
    def __init__(self, value, uncertainty):
        '''Takes a value +/- some uncertainty (stdev).'''
        self.x = value
        self.dx = np.abs(uncertainty) # for sanity

    def quad(self, a, b):
        return np.sqrt(np.square(a) + np.square(b))
    def rel_quad(self, ada, bdb):
        return np.sqrt(np.square(ada.dx/ada.x) + np.square(bdb.dx/bdb.x))

    def __neg__(self):
        v = -self.x
        u = self.dx
        return Quantity(v, u)

    def __add__(self, other):
        if(type(other) != Quantity):
            v = self.x + other
            u = self.dx
            return Quantity(v, u)
        v = self.x + other.x
        u = self.quad(self.dx, other.dx)
        return Quantity(v, u)
    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if(type(other) == Quantity):
            v = self.x - other.x
            u = self.quad(self.dx, other.dx)
        else:
            v = self.x - other
            u = self.dx
        return Quantity(v, u)
    def __rsub__(self, other):
        return -self.__sub__(other)

    def __mul__(self, other):
        if(type(other) == Quantity):
            v = self.x * other.x
            u = v * self.rel_quad(self, other)
        else:
            v = self.x * other
            u = self.dx
        return Quantity(v, u)
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if(type(other) == Quantity):
            v = self.x/other.x
            u = v * self.rel_quad(self, other)
        else:
            v = self.x / other
            u = self.dx
        return Quantity(v, u)
    def __rtruediv__(self, other):
        if(type(other)==Quantity):
            v = other.x/self.x
            u = v * self.rel_quad(self, other)
        else:
            v = other/self.x
            u = self.dx * other / np.square(self.x)
        return Quantity(u, v)

    def __pow__(self, n):
        v = np.pow(self.x, n)
        u = np.pow(self.x, n-1) * n * self.dx
        return Quantity(v, u)

    def __repr__(self):
        x = self.x
        dx = self.dx
        if(dx == 0):
            return f'{x}±{dx}'
        order = int(np.ceil(np.abs(np.log10(dx))) * np.sign(np.log10(dx)))
        order_a = np.abs(order)
        if(order < 0):
            return ("{:."+str(order_a)+"f}±{:."+str(order_a)+"f}").format(np.round(x, order_a), np.round(dx, order_a))
        else:
            return ("{:"+str(order_a)+"f}±{:"+str(order_a)+"f}").format(x, dx)