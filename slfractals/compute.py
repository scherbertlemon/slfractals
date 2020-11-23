import numpy as np
import re
from pathlib import Path


def poly_iter(poly, c, max_iter=100, max_value=2):
    z = np.zeros(c.shape, dtype=np.complex128)
    niter = np.zeros(c.shape, dtype=np.int64)
    for i in range(0, max_iter):
        i, j = np.where(np.abs(z) < max_value)
        z[i, j] = poly(z[i, j], c[i, j])
        niter[i, j] += 1
    return z, niter


def get_grid(xlim, ylim, resolution):
    x = np.linspace(*xlim, resolution[0])
    y = np.linspace(*ylim, resolution[1]) * 1.j

    X, Y = np.meshgrid(x, y)
    return X + np.flip(Y, axis=0)


def gradient_func(niter, absz, exp):
    i, j = np.where(niter < np.max(niter))
    grad = np.ones(niter.shape) * np.max(niter)
    grad[i, j] = niter[i, j] + 1 - np.log(np.log(absz[i, j]))/np.log(exp)
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