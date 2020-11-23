import numpy as np
import re
from pathlib import Path
import numpy as np
from multiprocessing import Pool


def split(arr, nportions=4):
    partsize = int(np.ceil(len(arr) / nportions))
    
    for n in range(0, nportions):
        nr = (n + 1) * partsize
        nright = nr if nr < len(arr) else len(arr)
        yield arr[n*partsize:nright]


def join(arr_list, nx, ny):
    return np.concatenate(arr_list).reshape((nx, ny))

def poly_iter_serial(poly, c, max_iter=100, max_value=2, nproc=2, nchunks=4):
    G, Z, niter = poly_iter(poly, c.flatten(), max_iter=max_iter, max_value=max_value)
    return (
        G.reshape(c.shape),
        Z.reshape(c.shape),
        niter.reshape(c.shape)
    )

def mandel(z, c):
    return z**2 + c

    
class Compute:
    def __init__(self, poly, max_iter=100, max_value=2):
        self.max_iter = max_iter
        self.max_value = max_value
        self.poly = poly

    def __call__(self, batch):
        return poly_iter(self.poly, batch, max_iter=self.max_iter, max_value=self.max_value)


def poly_iter_parallel(poly, c, max_iter=100, max_value=2, nproc=2, nchunks=4):

    with Pool(nproc) as P:
        all_results = P.map(
            Compute(poly, max_iter=100, max_value=2),
            split(c.flatten(), nportions=nchunks)
        )
    
    return (
        join([a[0] for a in all_results], *c.shape),
        join([a[1] for a in all_results], *c.shape),
        join([a[2] for a in all_results], *c.shape)
    )

# def poly_iter(poly, c, max_iter=100, max_value=2):
#     z = np.zeros(c.shape, dtype=np.complex128)
#     niter = np.zeros(c.shape, dtype=np.int64)
#     for it in range(0, max_iter):
#         i, j = np.where(np.abs(z) < max_value)
#         z[i, j] = poly(z[i, j], c[i, j])
#         niter[i, j] += 1
#     return z, niter


def poly_iter(poly, c, max_iter=100, max_value=2):
    z = np.zeros(c.shape, dtype=np.complex128)
    niter = np.zeros(c.shape, dtype=np.int64)
    for it in range(0, max_iter):
        i = np.where(np.abs(z) < max_value)
        z[i] = poly(z[i], c[i])
        niter[i] += 1
    return gradient_func(niter, np.abs(z)), z, niter


def get_grid(xlim, ylim, resw=1720, ratio=None):
    if ratio is None:
        resolution = (resw, int((ylim[1] - ylim[0]) / (xlim[1] - xlim[0]) * resw))
    else:
        resolution = (resw, int(resw * ratio))
        nratio = (xlim[1] - xlim[0]) * ratio
        ylim = (0.5*(sum(ylim) - nratio), 0.5*(sum(ylim) + nratio))

    x = np.linspace(*xlim, resolution[0])
    y = np.linspace(*ylim, resolution[1]) * 1.j

    X, Y = np.meshgrid(x, y)
    return X + np.flip(Y, axis=0)


def gradient_func(niter, absz):
    i = np.where(niter < np.max(niter))
    grad = np.ones(niter.shape) * np.max(niter)
    grad[i] = niter[i] + 1. - np.log(np.log(absz[i]))/np.log(2)
    return grad


def get_render_filename(loc):
    loc = Path(loc)
    loc.mkdir(exist_ok=True, parents=True)
    first = loc / "render-0000.png"
    if not first.exists():
        return first
    else:
        pat = re.compile("[0-9]+")
        files = sorted(loc.glob("render-*.png"), key=lambda p: int(pat.search(str(p)).group(0)), reverse=False)
        lasti = int(pat.search(str(files[-1])).group(0))
        # print(files)
        return loc / "render-{:04d}.png".format(lasti + 1)