from argparse import ArgumentParser
from .compute import *
from matplotlib import pyplot as plt
from matplotlib import cm
import sys


def mandelbrot():
    p = ArgumentParser(description="renders a plain view of the mandelbrot set as png")
    p.add_argument(
        "-l", "--left",
        type=float,
        help="left (real) boundary of the picture as float, default: -1.8",
        default=-1.8
    )
    p.add_argument(
        "-r", "--right",
        type=float,
        help="right (real) boundary of the picture as float, default: 0.67",
        default=0.67
    )
    p.add_argument(
        "-b", "--bottom",
        type=float,
        help="bottom (imaginary) boundary of the picture as float, default: -1.2",
        default=-1.2
    )
    p.add_argument(
        "-t", "--top",
        type=float,
        help="top (imaginary) boundary of the picture as float, default: 1.2",
        default=1.2
    )
    p.add_argument(
        "-w", "--width",
        help="desired resolution for width of picture in pixels, height is determined by coordinate ratio, default: 1280",
        type=int,
        default=1280
    )
    p.add_argument(
        "-i", "--max-iterations",
        help="Maximum iterations for data point before recursive computation is stopped",
        type=int,
        default=200
    )
    p.add_argument(
        "-v", "--max-value",
        help="Maximum value for which the iteration is stopped for a given data point",
        default=2
    )
    args = p.parse_args(sys.argv[1:])

    renderres = (args.width, int((args.top - args.bottom) / (args.right - args.left) * args.width))
    C = get_grid(
        (args.left, args.right),
        (args.bottom, args.top),
        renderres
    )

    Z, niter = poly_iter(
        lambda z, c: z**2 + c,
        C,
        max_iter=args.max_iterations,
        max_value=args.max_value
    )

    dpi = 300
    figs = plt.figure(num=2, figsize=(renderres[0]/dpi, renderres[1]/dpi), dpi=dpi)
    figs.clear()
    ax2 = figs.add_axes([0, 0, 1, 1])
    ax2.imshow(gradient_func(niter, np.abs(Z), 2), cmap=cm.hot)
    ax2.set_position((0, 0, 1, 1))
    plt.axis("off")
    plt.savefig(get_render_filename(Path.cwd()))


