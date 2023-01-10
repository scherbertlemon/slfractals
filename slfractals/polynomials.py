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
    return zpn(z, c, 2)


def zp5(z, c):
    return zpn(z, c, 5)


def zpn(z, c, n):
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