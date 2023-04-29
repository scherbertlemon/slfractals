from multiprocessing import Value
import numpy as np
from numpy.linalg import norm
from bokeh.plotting import ColumnDataSource


def koch_segment(line_segment):
    """
    From a line segment with 2 endpoints, generate 5 endpoints of the 4 line segments of one iteration of the koch curve.

    Parameters
    ----------
    line_segment: list of 2 2x1 numpy arrays
        endpoints of initial line segment .___.
    
    Returns
    -------
    list of 5 2x1 numpy arrays
        endpoints of line segments of koch curve ._./'\._.
    """

    endpoints = [p for p in line_segment]
    p1 = endpoints[0]
    p2 = endpoints[1]
    diff = p2 - p1
    length = norm(diff)
    m1 = p1 + diff / 3
    m2 = p2 - diff / 3
    turn = np.array([[0, -1], [1, 0]])
    m3 = p1 + 0.5 * diff + np.matmul(turn, diff) * 0.5 / np.sqrt(3)

    return np.array([p1, m1, m3, m2, p2])


def recursive_koch(points, levels=0):
    if levels == 0:
        return points
    else:
        more_points = np.vstack([koch_segment(points[i:i+2]) for i in range(0, points.shape[0] - 1)])
        final_points = recursive_koch(more_points, levels=levels - 1)
        return final_points


class KochCurve:

    def __init__(self, appearance="curve"):
        p1 = np.array((-1, 0))
        p2 = np.array((1, 0))
        if appearance == "curve":
            self.line = np.array((p1, p2))
        elif appearance == "snowflake":
            p3 = np.array((0, -np.sqrt(3)))
            self.line = np.array((p1, p2, p3, p1))
        else:
            raise ValueError("appearance must be 'curve' or 'snowflake'")

        self._cds = None
    
    @property
    def x(self):
        return self.line[:, 0]
    
    @property
    def y(self):
        return self.line[:, 1]

    @property
    def cds(self):
        if self._cds is None:
            self._cds = ColumnDataSource(data=dict(x=self.x, y=self.y))
        return self._cds

    def update_cds(self):
        self.cds.data = dict(x=self.x, y=self.y)
        return self.cds

    def increment(self, by=1):
        self.line = recursive_koch(self.line, levels=by)
        self.update_cds()
