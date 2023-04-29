"""
Some polynomials for recursive application on the complex plane.
The functions are implemented exlicitly in this form, as I did
not find another way to pickle them for parallel processing.
"""


def mandel(z, c):
    """
    The function to generate the mandelbrot set.

    Parameters
    ----------
    z: Complex
        scalar, vector or matrix to evaluate the function on elementwise
    c: Complex
        scalar, vector or matrix, the starting value(s)
    """
    return zpn(z, c)

def zp3(z, c):
    return zpn(z, c, n=3)

def zp4(z, c):
    return zpn(z, c, n=4)

def zp5(z, c):
    return zpn(z, c, n=5)


def zpn(z, c, n=2):
    """
    nth order polynomial generating a beautiful set

    Parameters
    ----------
    z: Complex
        scalar, vector or matrix to evaluate the function on elementwise
    c: Complex
        scalar, vector or matrix, the starting value(s)
    """
    return z**n + c


def poly1(z, c):

    return z**3 - 3* (c+0.5j)**2*z + c