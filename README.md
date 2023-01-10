# Exploring fractals with ``slfractals``

![banner](./doc/pics/banner.jpg)

This python package lets you explore fractals defined on the complex number plane.

**!!! This is an early version: documentation, functionality and interfaces are not perfect and will change in the future. !!!**

## Running on Docker

That's the easiest way. Clone the repository, then from this folder, build image with:

    docker build -t slfractals:latest .

To run the bokeh app, run:

    docker run --rm -it -p 5006:5006 slfractals:latest


## Installation and setup

**It is recommended to use ``conda`` on Windows to install dependencies for this package.**

1. **Clone** or download [the ``slfractals`` repository](https://github.com/scherbertlemon/slfractals)
2. **Creating a python environment** with [``conda``](https://docs.conda.io/en/latest/miniconda.html) and the ``requirements.txt`` file in the locally cloned or downloaded folder (recommended on Windows):

        conda create -n fractals python=3.8 --file requirements.txt

    You can activate your environment with
    
        conda activate fractals
    
3. **Install** ``slfractals`` into your python environment: Activate the environment and run in your locally cloned or downloaded folder

        pip install -e .

View ``requirements.txt`` to see the python packages used by the ``slfractals`` package. It is read during the setup, and ``pip`` should handle the dependencies for you (not correctly on Windows).

This package cannot yet be obtained from any python repo source, so the development install outlined above is the way to go for now.

## Usage

Functionality is mostly encapsulated in the ``slfractals`` module.
* **NEW**: There is a preliminary bokeh app, that can be like

        bokeh serve --show notebooks/fractall.py

* For exploring there is a Jupyter notebook, where you can zoom into a fractal set and render high-resolution pictures on demand: [explore.ipynb](notebooks/explore.ipynb).
* To render pictures directly in a specific region of the mandelbrot set, use the command line script from a terminal with activated python environment:

        >>> mandelbrotset -h
        usage: mandelbrotset [-h] [-l LEFT] [-r RIGHT] [-b BOTTOM] [-t TOP] [-w WIDTH] [-i MAX_ITERATIONS] [-v MAX_VALUE]

        renders a plain view of the mandelbrot set as png

        optional arguments:
        -h, --help            show this help message and exit
        -l LEFT, --left LEFT  left (real) boundary of the picture as float, default: -1.8
        -r RIGHT, --right RIGHT
                                right (real) boundary of the picture as float, default: 0.67
        -b BOTTOM, --bottom BOTTOM
                                bottom (imaginary) boundary of the picture as float, default: -1.2
        -t TOP, --top TOP     top (imaginary) boundary of the picture as float, default: 1.2
        -w WIDTH, --width WIDTH
                                desired resolution for width of picture in pixels, height is determined by coordinate ratio, default: 1280
        -i MAX_ITERATIONS, --max-iterations MAX_ITERATIONS
                                Maximum iterations for data point before recursive computation is stopped
        -v MAX_VALUE, --max-value MAX_VALUE
                                Maximum value for which the iteration is stopped for a given data point