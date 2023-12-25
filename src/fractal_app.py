from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Button, TextInput, Select, Div
from bokeh.plotting import figure
from bokeh.palettes import inferno, RdYlGn
from bokeh.layouts import column, row
import slfractals as slf
from time import time, sleep
import numpy as np
from inspect import getmembers, isfunction
from slfractals.colors import blueorangeblue

NPROC = 4

xlim = (-1.8, 1.)
ylim = (-0.9, 0.9)

resw = 900
factor = 1
C = slf.get_grid(xlim, ylim, resw=resw)

grad = slf.parallel_compute(
    slf.mandel,
    C,
    max_iter=300,
    max_value=5,
    colorexp=2,
    nproc=NPROC
)

p = figure(
    title="fractal",
    width=grad.shape[1]*factor,
    height=grad.shape[0]*factor,
    x_range=xlim,
    y_range=ylim
)

polys = dict(getmembers(slf.polynomials, isfunction))
polyselect = Select(title="Choose polynomial", value="mandel", options=list(polys.keys()), width=int(0.5*resw))

niter_field = TextInput(value="300", title="Maximum iterations", width=int(0.5*resw))
b = Button(label="Calculate")
range_format = '{{"xlim": ({}, {}), "ylim": ({}, {})}}'
range_output = Div(text=range_format.format(C.real.min(), C.real.max(), C.imag.min(), C.imag.max()))

cds = ColumnDataSource(data=dict(
    image=[np.flip(grad, axis=0)],
    x=[xlim[0]], y=[ylim[0]],
    dw=[xlim[1]-xlim[0]], dh=[ylim[1]-ylim[0]]
))

img = p.image(
    image="image",
    x="x",
    y="y",
    dw="dw",
    dh="dh",
    source=cds,
    palette=blueorangeblue(100)
)

refresh = {"time": time()}



def update():

    nxlim = (p.x_range.start, p.x_range.end)
    nylim = (p.y_range.start, p.y_range.end)
    # print(old, new)
    print(f"x: {nxlim}")
    print(f"y: {nylim}")

    start = time()

    C = slf.get_grid(
        nxlim,
        nylim,
        resw=resw
    )

    range_output.text = range_format.format(C.real.min(), C.real.max(), C.imag.min(), C.imag.max())
    print(f"mesh: {C.shape}")
    try:
        niter = int(niter_field.value)

        if niter < 1:
            print("niter must be bigger than 1")
            niter = 2
        elif niter > 5000:
            print("niter should be < 5000 if calc should finish within years.")
            niter = 5000
    except ValueError as ve:
        print("invalid value for number of iterations, back to standard 300")
        niter = 300

    
    grad = slf.parallel_compute(
        polys[polyselect.value],
        C,
        max_iter=niter,
        max_value=5,
        colorexp=2,
        nproc=NPROC
    )
    end = time()
    print(f"refreshtime = {end-start}s")
    print(f"{grad.shape}")
    cds.data = dict(
        image=[np.flip(grad, axis=0)],
        x=[nxlim[0]], y=[nylim[0]],
        dw=[nxlim[1]-nxlim[0]], dh=[nylim[1]-nylim[0]]
    )
    p.width=grad.shape[1]*factor
    p.height=grad.shape[0]*factor
    refresh["time"] = time()
    
    return grad, C
    # p.plot_height = grad.shape[1]


def update_timed(attr, old, new):
    if time() - refresh["time"] > 3:
        update()
    else:
        pass
        # print("no refresh")

def update_always(event):
    update()

# def update_render(event):
#     grad, _ = update(resw=1920)
#     file = slf.render_picture(
#         grad,
#         "files"
#     )

# renderb = Button(label="render")
# renderb.on_click(update_render)
b.on_click(update_always)
p.y_range.on_change("end", update_timed)

curdoc().add_root(column(row(polyselect, niter_field), b, range_output, p))