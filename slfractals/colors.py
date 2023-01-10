import numpy as np
from functools import reduce

def blueorangeblue(n=10):
    origin_colors = [
        "#000000",
        "10006D",
        "6D0037",
        "DE3C00",
        "DE7100",
        "FEB828",
        "FCF7EC",
        "93C2FC",
        "0073FF",
        "001D41"
    ]
    origin_colors.reverse()
    cg = ColorGradient(origin_colors)
    return cg(n)


class BernsteinPoly:

    @classmethod
    def get_poly(cls, n, k):
        if k < 0 or k > n:
            raise ValueError(f"tried to get the {k}th polynomial of order {n}")
        return lambda t: np.math.comb(n, k) * t**k * (1 - t)**(n - k)

    @classmethod
    def all_polynomials(cls, n):
        return [cls.get_poly(n, k) for k in range(0, n+1)]


class BezierSpline(BernsteinPoly):

    def __init__(self, control_points):
        self.p = control_points

    
    @property
    def n(self):
        return self.p.shape[0] - 1
    
    @property
    def dim(self):
        return self.p.shape[1]

    def calculate(self, n_discr=100):
        t = np.linspace(0, 1, n_discr)
        poly_evaluated = np.array([poly(t) for poly in self.all_polynomials(self.n)])
        
        all_t_dim = []
        for dim in range(0, self.dim):
            all_t_dim.append(np.matmul(poly_evaluated.T, self.p[:, dim]))
        
        return np.array(all_t_dim).T


class ColorGradient:

    def __init__(self, hex_list):
        self.origin_colors = hex_list

    @classmethod
    def remove_hashtag(cls, hex_list):
        return [h[1:] if h[0] == "#" else h for h in hex_list]

    @classmethod
    def triples(cls, hex_list):
        return np.array([tuple(h[i:i+2] for i in range(0, len(h) - 1, 2)) for h in cls.remove_hashtag(hex_list)])
    
    @classmethod
    def hex_str_to_int(cls, str_array):
        return np.vectorize(lambda n: int(n, 16))(str_array)

    @classmethod
    def int_triples_to_hex_str(cls, int_triples):
        hexes = []
        for m in range(0, int_triples.shape[0]):
            triple = [hex(a).upper() for a in int_triples[m, :]]
            triple = [t[2:] if len(t) > 3 else "0" + t[2:] for t in triple]
            hexes.append("#" + "".join(triple))
            # hexes.append(triple)

        return hexes

    @property
    def ints(self):
        return self.hex_str_to_int(self.triples(self.origin_colors))

    def __call__(self, n):
        bs = BezierSpline(self.ints)
        colors = bs.calculate(n_discr=n).astype(int)
        return tuple(self.int_triples_to_hex_str(colors))

