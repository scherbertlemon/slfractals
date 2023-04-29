# Exploring fractals with ``slfractals``

![banner](./doc/pics/banner.jpg)

This python package lets you explore fractals defined on the complex number plane. Therefore, it packages a bokeh app and some Jupyter notebooks, that can be run with docker compose.

## Requirements

* Working docker installation.

## Usage

1. Clone or download [the ``slfractals`` repository](https://github.com/scherbertlemon/slfractals)
2. Run the fractal visualization app and a Jupyter server to explore the notebooks by entering in a terminal in the local project folder

    ```bash
    docker compose up
    ```
    
3. Access the ``bokeh`` app in your web browser at http://localhost:5006/fractal_app
4. Access the Jupyter server and the notebooks in your web browser at http://localhost:8888/tree?token=mandelbr0t
5. Run
    ```bash
    docker compose down
    ````
    to shut down the app and notebook server and clean up all containers.

For development, you can also run a development container in VSCode, based on the settings in ``.devcontainer``.
