from pathlib import Path
import re
from matplotlib import pyplot as plt
from matplotlib import cm


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
