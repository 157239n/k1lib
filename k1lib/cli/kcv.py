# AUTOGENERATED FILE! PLEASE DON'T EDIT HERE. EDIT THE SOURCE NOTEBOOKS INSTEAD
"""
This includes helper clis that make it quick to graph graphviz plots."""
__all__ = ["markers", "Markers", "map3d"]
import re, k1lib, math, os, numpy as np, io, json, base64, html
from k1lib.cli.init import BaseCli; import k1lib.cli as cli, k1lib.cli.init as init
cv2 = k1lib.dep("cv2", "opencv-python", "https://opencv.org/")
aruco = k1lib.dep("cv2.aruco", "opencv-python", "https://opencv.org/")
from collections import deque, defaultdict
settings = k1lib.settings.cli
class markers(BaseCli):                                                          # markers
    def __init__(self, d:str=None):                                              # markers
        """Detect aruco markers. Returns :class:`Markers`.
Example::

    im = "some/image.jpg" | toImg()
    markers = im | kcv.markers()

    markers # run this in a notebook cell to quickly view where the bounding boxes are
    markers | item() # grab first detection, a tuple (aruco dictionary, coords (with shape (4,2)), number)
    markers[0] # same as above
    markers | deref() # dereference into just lists, instead of kcv.Markers object

For a moderately complex scene with 20 markers of size (1000, 800), this should take ~15ms to run. The same
scene of size (4000, 3000) should take ~170ms to run

:param d: aruco dictionary string, like 'DICT_7X7_1000'. If specified, then will only look in
    those dictionaries. If not specified will look in all dictionaries"""        # markers
        self.ds = [d] if d else ["DICT_4X4_1000", "DICT_5X5_1000", "DICT_6X6_1000", "DICT_7X7_1000"] # markers
    def __ror__(self, im):                                                       # markers
        arr = im | cli.toNdArray(np.uint8) | cli.op().transpose(1, 2, 0)         # markers
        return Markers(im, self.ds | cli.apply(lambda d: [d, cv2.aruco.detectMarkers(arr, aruco.Dictionary_get(getattr(aruco, d)))[:2]]) | cli.deref() | ~cli.filt("x[1] is None", 1) | cli.apply(cli.item().all(2) | cli.T() , 1) | cli.ungroup(False) | cli.deref()) # markers
class Markers:                                                                   # Markers
    def __init__(self, im, ms):                                                  # Markers
        """Resulting Markers object, obtained from :class:`markers` cli, not
intended to be instantiated by the end user."""                                  # Markers
        self.im = im; self._ms = ms                                              # Markers
    def __getitem__(self, s): return self._ms[s]                                 # Markers
    def __iter__(self): return iter(self._ms)                                    # Markers
    def __len__(self): return len(self._ms)                                      # Markers
    def __repr__(self): return f"<Markers n={len(self)} im.shape={self.im | cli.shape() | cli.op()[::-1]} ds={self._ms | cli.cut(0) | cli.count() | ~cli.sort() | cli.cut(1) | cli.deref()}>" # Markers
    def _repr_html_(self):                                                       # Markers
        im = self.im; ms = self._ms; p5 = k1lib.p5; p5.newSketch(*im | cli.shape(), False) # Markers
        p5.image(im, 0, 0); p5.background(200, 220)                              # Markers
        for _dict, coords, num in ms:                                            # Markers
            a,b,c,d = coords                                                     # Markers
            p5.stroke(255, 0, 0);   p5.line(*a,*b)                               # Markers
            p5.stroke(0, 255, 0);   p5.line(*b,*c)                               # Markers
            p5.stroke(0, 0, 255);   p5.line(*c,*d)                               # Markers
            p5.stroke(255, 255, 0); p5.line(*d,*a)                               # Markers
            p5.stroke(255, 0, 255); p5.text(f"{num}", *a)                        # Markers
        return f"{html.escape(self.__repr__())}<br>{p5.svg()}"                   # Markers
def map3d(ws,cs):                                                                # map3d
    """Creates 2 functions that maps from world points (ws) to camera points (cs).
Example::

    ws = np.random.randn(10, 3)
    cs = np.copy(ws); cs[:,1] = -cs[:,1]; cs[:,2] = -cs[:,2]

    f1, f2 = kcv.map3d(ws, cs)

    f1(ws) # returns matrix similar to cs
    f2(cs) # returns matrix similar to ws
"""                                                                              # map3d
    wc = np.mean(ws, axis=0); wsp = ws - wc                                      # map3d
    cc = np.mean(cs, axis=0); csp = cs - cc                                      # map3d
    H = wsp.T @ csp; U, S, Vt = np.linalg.svd(H)                                 # map3d
    R = np.dot(U, Vt); R_inv = np.linalg.inv(R)                                  # map3d
    t = cc - np.dot(R, wc)                                                       # map3d
    # main equation is given by chatgpt, but the transformation for some reason is translated by a # map3d
    # fixed vector, so this is to figure out the correct bias vector to add to   # map3d
    b1 = cc-(ws@R+t) | cli.T() | cli.toMean().all()                              # map3d
    b2 = ws-(cs-t)@R_inv | cli.T() | cli.toMean().all()                          # map3d
    return lambda vs: (vs)@R+t+b1, lambda vs: (vs-t)@R_inv+b2                    # map3d