from setuptools import setup, find_packages
from pathlib import Path
import re


def get_requirements():
    req_file = Path(__file__).parent / "requirements.txt"
    with open(req_file, "r") as req:
        reqs = [r.strip() for r in re.split("\r?\n", req.read()) if r]
    return reqs


setup(
    name="slfractals",
    version="0.2",
    description="exploring fractals defined on the complex number plane",
    author="Andreas Roth",
    url="https://github.com/scherbertlemon/slfractals",
    download_url="https://github.com/scherbertlemon/slfractals",
    packages=find_packages(),
    license="MIT License",
    keywords=["fractal", "complex", "mandelbrot"],
    install_requires=get_requirements(),
    zip_safe=True,
    entry_points={
        "console_scripts": [
            "mandelbrotset = slfractals.cli:mandelbrot"
        ]
    }
)
