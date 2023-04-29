from pathlib import Path
import re
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
from bokeh.plotting import figure, ColumnDataSource
from .colors import blueorangeblue
from .compute import serial_compute, get_grid, parallel_compute
from .polynomials import mandel



class Fractal:

    def __init__(self, xlim=(-1.5, 0.5), ylim=(-1.2, 1.2), poly=mandel, calc_fun=parallel_compute, resw=300, **kwargs):

        self._xlim = xlim
        self._ylim = ylim
        self._resw = resw
        self._p = None
        
        self.comp_param = kwargs
        self.calc_fun = calc_fun

        self._poly = poly

        self._cds = None
        self._grid = None

    @property
    def xlim(self):
        return self._xlim
    @xlim.setter
    def xlim(self, new_lim):
        self._xlim = new_lim
        self._grid = None
        self._cds.data = self.cds_data

    @property
    def ylim(self):
        return self._ylim
    @ylim.setter
    def ylim(self, new_lim):
        self._ylim = new_lim
        self._grid = None
        self._cds.data = self.cds_data

    @property
    def resw(self):
        return self._resw
    @resw.setter
    def resw(self, new_res):
        self._res = new_res
        self._grid = None
        self._cds.data = self.cds_data

    @property
    def grid(self):
        if self._grid is None:
            self._grid = get_grid(self.xlim, self.ylim, resw=self.resw)
        return self._grid

    @property
    def poly(self):
        return self._poly
    
    @poly.setter
    def poly(self, new_poly):
        self._poly = new_poly
        self._cds.data = self.cds_data
    
    @property
    def img(self):
        return self.calc_fun(self.poly, self.grid, **self.comp_param)

    @property
    def cds_data(self):
        return {
            "image": [np.flip(self.img, axis=0)],
            "x": [self.xlim[0]],
            "y": [self.ylim[0]],
            "dw": [self.xlim[1]-self.xlim[0]],
            "dh": [self.ylim[1]-self.ylim[0]]
        }

    @property
    def cds(self):
        if self._cds is None:
            self._cds = ColumnDataSource(
                data=self.cds_data
            )
        return self._cds

    def plot(self, palette=None):
        if palette is None:
            palette = blueorangeblue(100)
        img = self.img
        p = figure(
            plot_width=img.shape[1],
            plot_height=img.shape[0],
            x_range=self.xlim,
            y_range=self.ylim
        )
        p.image(image="image", source=self.cds, x="x", y="y", dw="dw", dh="dh", palette=palette)
        p.axis.visible = False
        p.toolbar.logo = None
        p.toolbar_location = None
        self.p = p
        return p



def get_render_filename(loc, nameroot="render"):
    loc = Path(loc)
    loc.mkdir(exist_ok=True, parents=True)
    first = loc / (nameroot + "-0000.png")
    if not first.exists():
        return first
    else:
        pat = re.compile("[0-9]+")
        files = sorted(loc.glob( nameroot + "-*.png"), key=lambda p: int(pat.search(str(p)).group(0)), reverse=False)
        lasti = int(pat.search(str(files[-1])).group(0))
        # print(files)
        return loc / "{}-{:04d}.png".format(nameroot, lasti + 1)


def render_picture(matrix, loc, dpi=300, cmap=cm.hot):
    figs = plt.figure(num=2, figsize=(matrix.shape[1]/dpi, matrix.shape[0]/dpi), dpi=dpi)
    figs.clear()
    ax2 = figs.add_axes([0, 0, 1, 1])
    ax2.imshow(matrix, cmap=cmap)
    ax2.set_position((0, 0, 1, 1))
    plt.axis("off")
    filename = get_render_filename(loc)
    plt.savefig(filename)
    return filename
