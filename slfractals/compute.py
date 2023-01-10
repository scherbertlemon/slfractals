import numpy as np
import re
from pathlib import Path
from multiprocessing import Pool
import functools


def sequence(func, z=0, n=0):
    if n == 0:
        return (z,)
    else:
        return (z, *sequence(func, z=func(z), n=n-1))


def split(arr, nportions=4):
    partsize = int(np.ceil(len(arr) / nportions))
    
    for n in range(0, nportions):
        nr = (n + 1) * partsize
        nright = nr if nr < len(arr) else len(arr)
        yield arr[n*partsize:nright]


def join_shape(arr_list, nx, ny):
    return np.concatenate(arr_list).reshape((nx, ny))


# def poly_iter_serial(poly, c, max_iter=100, max_value=2, nproc=2, nchunks=4):
#     G, Z, niter = poly_iter(poly, c.flatten(), max_iter=max_iter, max_value=max_value)
#     return (
#         G.reshape(c.shape),
#         Z.reshape(c.shape),
#         niter.reshape(c.shape)
#     )

  
class Compute:
    def __init__(self, poly, max_iter=100, max_value=2, colorexp=2):
        self.max_iter = max_iter
        self.max_value = max_value
        self.colorexp = colorexp
        self.poly = poly

        self.z = None
        self.niter = None

    def compute(self, batch):
        # print("compute")
        self.z, self.niter = poly_iter(
            self.poly,
            batch,
            max_iter=self.max_iter,
            max_value=self.max_value
        )

    @property
    def gradient(self):
        return gradient_func(self.niter, np.abs(self.z), self.colorexp)

    def __call__(self, batch):
        self.compute(batch)
        return self.gradient, self


def split_compute_join(func):
    @functools.wraps(func)
    def wrapper(poly, c, max_iter=100, max_value=2, nproc=2, colorexp=2):
        comp = Compute(poly, max_iter=max_iter, max_value=max_value, colorexp=colorexp)
        spl = split(c.flatten(), nportions=nproc*2)
        all_results = func(comp, spl, nproc)
        grads, _ = zip(*all_results)
        return join_shape(grads, *c.shape)
    return wrapper


@split_compute_join
def parallel_compute(comp, spl, nproc):
    with Pool(nproc) as P:
        all_results = P.map(comp, spl)
    return all_results


@split_compute_join
def serial_compute(comp, spl, nproc):
    return map(comp, spl)


def poly_iter(poly, c, max_iter=100, max_value=2):
    z = np.zeros(c.shape, dtype=np.complex128)
    niter = np.zeros(c.shape, dtype=np.int64)
    for it in range(0, max_iter):
        i = np.where(np.abs(z) < max_value)
        z[i] = poly(z[i], c[i])
        niter[i] += 1
    return z, niter


def get_grid(xlim, ylim, resw=1280, ratio=None):
    """
    Parameters
    ----------
    xlim: 2-tuple of float
        min and max value on x (real) axis
    ylim: 2-tuple of float
        min and max value on y (imaginary) axis
    resw: int
        resolution for the "width" of the picture, i.e. number of
        discretization points on the x (real) axis
    ratio: str
        of format e.g. "16:9"
        if given, adapts ylim (y-axis, imaginary) in a way that it matches the
        aspect ratio given by xlim and ratio. the resolution in y direction is
        also determined from the resulting ylim, ratio and resw. If not given,
        he aspect ratio is controlled by the values given in ylim compared to
        xlim.

    Returns
    -------
    numpy.ndarray :
        Matrix of complex values with boundaries xlim on real and ylim on
        imaginary axis

    Examples
    --------
    To render a picture in aspect ratio 16:9 with resolution 1280x720,
    generate a grid like this:

    >>> C = get_grid((-1., 1.), (-1., 1.), ratio="16:9", resw=1280)

    The value for ylim does not matter in this case. If you use

    >>> C = get_grid((-1., 1.), (-1., 1.), resw=300)

    you get a square 300x300 grid.
    """
    if ratio is None:
        resolution = (resw, int((ylim[1] - ylim[0]) / (xlim[1] - xlim[0]) * resw))
    else:
        mat = re.search("([0-9]+):([0-9]+)", ratio)
        r1 = float(mat.group(1))
        r2 = float(mat.group(2))
        resolution = (resw, int(resw * r2 / r1))
        nratio = (xlim[1] - xlim[0]) * r2 / r1
        ylim = (0.5*(sum(ylim) - nratio), 0.5*(sum(ylim) + nratio))

    x = np.linspace(*xlim, resolution[0])
    y = np.linspace(*ylim, resolution[1]) * 1.j

    X, Y = np.meshgrid(x, y)
    return X + np.flip(Y, axis=0)


def gradient_func(niter, absz, exp):
    i = np.where(niter < np.max(niter))
    grad = np.ones(niter.shape) * np.max(niter)
    grad[i] = niter[i] + 1. - np.log(np.log(absz[i]))/np.log(exp)
    return grad


