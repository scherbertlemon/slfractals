from pathlib import Path
import re


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