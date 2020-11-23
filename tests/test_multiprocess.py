import slfractals as sl
from time import time
from multiprocessing import Pool
import numpy as np

ma = 600

def poly(z, c):
    return z**2 + c

def compute(b):
    return sl.poly_iter(poly, b, max_iter=ma)

def main():
    xb = (-1.8, 0.67)
    yb = (-1.2, 1.2)
    w = 256
    C = sl.get_grid(xb, yb, resw=w)
    print(C.shape)
   
    # classic run:
    start = time()
    G1, Z1, niter1 = sl.poly_iter_serial(lambda z, c: z**2 + c, C, max_iter=ma)
    print("Normal run took: {:.4f}s".format(time() - start))

    # flatten, split, join
    start = time()
    collectz = []
    collectn = []
    for batch in sl.split(C.flatten()):
        G, Z, niter = sl.poly_iter_serial(lambda z, c: z**2 + c, batch, max_iter=ma)
        # print(Z)
        collectz.append(Z)
        collectn.append(niter)
    Z2 = sl.join(collectz, *C.shape)
    # print(Z2)
    niter2 = sl.join(collectn, *C.shape)
    print("Split run took: {:.4f}s".format(time() - start))

    # multiprocess
    start = time()
    collectz = []
    collectn = []
    with Pool(4) as p: 
        parres = p.map(sl.Compute(lambda z, c: z**2 + c, max_iter=ma), sl.split(C.flatten()))
    Z3 = sl.join([pp[1] for pp in parres], *C.shape)
    # print(Z3)
    niter3 = sl.join([pp[2] for pp in parres], *C.shape)
    print("Parallel run took: {:.4f}s".format(time() - start))

    print(np.any(np.abs(Z1-Z2)>1e-15))
    print(np.any(np.abs(Z2-Z3)>1e-15))
    print(np.any(np.abs(Z1-Z3)>1e-15))
if __name__ == "__main__":
    main()
