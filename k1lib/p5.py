# AUTOGENERATED FILE! PLEASE DON'T EDIT HERE. EDIT THE SOURCE NOTEBOOKS INSTEAD
"""A quick and dirty tiny module emulating the `p5js <https://p5js.org/>`_
environment. I made this because I have used Processing extensively in
the past, and would like a simple interface to draw stuff. Processing
doesn't really exist on Python (yes, I know of Processing's python mode,
but it's Jython, not pure python!), so I made this based upon the
`drawsvg <https://github.com/cduck/drawSvg>`_ library. Download that
before using this module. Example::

    from k1lib.imports import *

    p5.newSketch(200, 200); p5.background(150)
    p5.rect(0, 0, 60, 60)
    with p5.context(): # all style changes here will be reverted on exiting the context
        p5.fill(255, 0, 0)
        p5.rect(0, 0, 60, 50)
    p5.rect(0, 0, 30, 30)
    p5.fill(255, 180); p5.ellipse(60, 50, 20)
    p5.textSize(12); p5.text("abc", 30, 30)
    with p5.context():
        p5.fill(0, 0, 255); p5.noStroke(); p5.textSize(20)
        p5.text("def", 60, 60)
    p5.img() # get PIL image

Result:

.. image:: images/p5.png"""
import k1lib, math, numpy as np, random, base64, json; import k1lib.cli as cli; from typing import List, Iterator
from collections import defaultdict, deque
drawsvg = k1lib.dep("drawsvg", "drawsvg[all]", "https://github.com/cduck/drawSvg")
__all__ = ["color", "newSketch", "fill", "noFill", "stroke", "noStroke", "ellipse", "arc", "rect", "textSize", "text", "background", "img",
           "Entity", "Point", "point_raw", "point_rnd", "point_sym", "point_L", "triangle",
           "Line", "line_2P", "line_2PL", "Circle", "circle_PR", "circle_2P", "grid", "axes", "IR",
           "Sketch"]
def color(r, g=None, b=None, alpha=255):                                         # color
    """Get hex representation of a color.
Example::

    p5.color(255, 0, 0) # returns "#ff0000ff", red
    p5.color(255, 0, 0, 100) # returns "#ff000064", transparent red
    p5.color(255, 100) # returns "#ffffff64", transparent white"""               # color
    if isinstance(r, str):                                                       # color
        if g is not None or b is not None: raise Exception(f"Doesn't understand this color specification: {r}, {g}, {b}, {alpha}") # color
        r = "#" + r.strip("#")                                                   # color
        if len(r) == 7: return r + "ff"                                          # color
        elif len(r) == 9: return r                                               # color
        else: raise Exception(f"Doesn't understand this string color: {r}")      # color
    if g is None and b is None: g = r; b = r                                     # color
    if g is not None and b is None: alpha = g; g = r; b = r                      # color
    return f"#{r:02x}{g:02x}{b:02x}{alpha:02x}"                                  # color
c = k1lib.Settings();                                                            # color
context = c.context                                                              # color
def _strokeAlpha(): return int(c.stroke[-2:], 16) if c.stroke else 255           # _strokeAlpha
def _fillAlpha(): return int(c.fill[-2:], 16) if c.fill else 255                 # _fillAlpha
def _alpha(): return min(_strokeAlpha(), _fillAlpha())                           # _alpha
def _cs(): return {"fill": c.fill, "stroke": c.stroke, "fill_opacity": _fillAlpha()/255, "stroke_opacity": _strokeAlpha()/255} # colors shorthand # _cs
def newSketch(w, h, flip=True, pad=0, scale=1, xoff=0, yoff=0):                  # newSketch
    """Creates a new sketch with specified height and width.

If ``pad``, ``scale``, ``xoff`` or ``yoff`` is specified, it will pad the sketch then scale it up with
that amount. In other words, the true width (in pixels) is going to be ``w*scale + 2*pad``, true height
is ``h*scale + 2*pad``. Then, all coordinates will be ``(x-xoff)*scale + pad`` and ``(y-yoff)*scale + pad``,
and any radius/size will be ``r*scale``.

:param flip: if True (default), use mathematical coordinate (y increases from bottom of image to top), else use
    programming coordinate (y increases from top of image to bottom). This only affects the y axis,
    leaving x axis and radiuses alone
:param xoff: x offset. If specified, along side with yoff, then the sketch will have the
    point (xoff,yoff) at origin
"""                                                                              # newSketch
    c.d = drawsvg.Drawing(w*scale+2*pad, h*scale+2*pad); c.w = w; c.h = h        # newSketch
    c.stroke = color(0); c.fill = color(255); c.fontSize = 12; c.flip = flip; c.pad = pad; c.scale = scale # newSketch
    c.xt = lambda x: (x-xoff)*scale+pad; c.rt = lambda r: r*scale                # newSketch
    if flip: c.yt = lambda y: (h-(y-yoff))*scale+pad; c.ht = lambda h: -h*scale # y transform and h transform # newSketch
    else: c.yt = lambda y: (y-yoff)*scale+pad; c.ht = lambda h: h*scale          # newSketch
def fill(*args):                                                                 # fill
    """Sets fill color"""                                                        # fill
    c.fill = color(*args)                                                        # fill
def noFill():                                                                    # noFill
    """Turns off fill color"""                                                   # noFill
    c.fill = color(255, 0)                                                       # noFill
def stroke(*args):                                                               # stroke
    """Sets stroke color"""                                                      # stroke
    c.stroke = color(*args)                                                      # stroke
def noStroke():                                                                  # noStroke
    """Turns off stroke color"""                                                 # noStroke
    c.stroke = color(255, 0)                                                     # noStroke
def ellipse(x, y, w):                                                            # ellipse
    """Draws a circle at a particular location. Can't truly draw ellipses cause idk how""" # ellipse
    c.d.append(drawsvg.Circle(c.xt(x), c.yt(y), c.rt(w/2), **_cs()))             # ellipse
pi = 3.141592653589793                                                           # ellipse
def arc(x, y, r, startAngle, endAngle):                                          # arc
    """Draws an arc.

If in mathematical coordinates, will go counter clockwise from startAngle to endAngle.
If in programming coordinates, will go counter clockwise instead.

If startAngle < endAngle, and the difference between them is also pretty small (say 45deg),
then the sweep angle will also be small. If startAngle > endAngle, then the sweep angle
is going to be very big (360-45)"""                                              # arc
    f = (1-2*c.flip)*180/pi; c.d.append(drawsvg.Arc(c.xt(x), c.yt(y), c.rt(r), startAngle*f, endAngle*f, cw=f>0, **_cs())) # arc
def line(x1,y1,x2,y2):                                                           # line
    """Draws a line from (x1, y1) to (x2, y2)"""                                 # line
    c.d.append(drawsvg.Line(c.xt(x1),c.yt(y1),c.xt(x2),c.yt(y2),**_cs()))        # line
def image(img:"PIL", x, y, w=None, h=None):                                      # image
    """Draws a PIL image at a particular position.
Example::

    img = "image_file.png" | toImg()
    p5.newSketch(400, 200)
    p5.image(img, 20, 20)

You can transform it first using torchvision.transforms before drawing it like this::

    img = "image_file.png" | toImg()
    img = img | aS(tf.Resize(200)) # torchvision.transforms is imported as `tf` automatically. Check module `k1lib.imports`
"""                                                                              # image
    s = img | cli.shape(); c.d.append(drawsvg.Image(c.xt(x), c.yt(y), c.rt(w or s[0]), c.rt(h or s[1]), f'data:image/png;base64,{img | cli.toBytes() | cli.aS(base64.b64encode) | cli.op().decode()}')) # image
def rect(x, y, w, h, r=0):                                                       # rect
    """Draws a rectangle.

:param r: border radius"""                                                       # rect
    if r == 0: c.d.append(drawsvg.Rectangle(c.xt(x), c.yt(y), c.rt(w), c.ht(h), **_cs())) # rect
    else:                                                                        # rect
        c.d.append(drawsvg.Path(**_cs())                                         # rect
           .arc(c.xt(x+r), c.yt(y+r), r, 90, 180)                                # rect
           .arc(c.xt(x+r), c.yt(y+h-r), r, 180, 270, includeL=True)              # rect
           .arc(c.xt(x+w-r), c.yt(y+h-r), r, 270, 0, includeL=True)              # rect
           .arc(c.xt(x+w-r), c.yt(y+r), r, 0, 90, includeL=True).L(x+r, c.yt(y))) # rect
def textSize(s):                                                                 # textSize
    """Sets the text size. This is affected by the global scaling factor specified in :meth:`newSketch`""" # textSize
    c.fontSize = s                                                               # textSize
def text(s, x, y):                                                               # text
    """Draws text at a specific location."""                                     # text
    c.d.append(drawsvg.Text(s, c.rt(c.fontSize), c.xt(x), c.yt(y), **_cs()))     # text
def background(*args):                                                           # background
    """Changes the background color"""                                           # background
    with c.context(stroke=color(*args), fill=color(*args)): c.d.append(drawsvg.Rectangle(0, 0, (c.w+2*c.pad)*c.scale, (c.h+2*c.pad)*c.scale, **_cs())) # background
def img():                                                                       # img
    """Returns a PIL image of the sketch"""                                      # img
    return c.d.rasterize().png_data | cli.toImg()                                # img
def svg() -> str:                                                                # svg
    """Returns svg string of the sketch"""                                       # svg
    return c.d.as_svg()                                                          # svg
inf = float("inf")                                                               # svg
class Entity(cli.BaseCli):                                                       # Entity
    def __init__(self, *args):                                                   # Entity
        """Geometry-building package.

So, within p5 module, there's sort of like a submodule that deals with geometrical data
that allows you to define things like in Geogebra, whose work I'm a huge fan of. Here's
how it works::

    # creates an IR (intermediate representation) that defines 2 points and a line connecting the 2 points
    ir = None | p5.point_raw("P1", 3, 4) | p5.point_raw("P2", 5, 8) | p5.line_2P("L1", "P1", "P2")
    # calculates the exact position of all entities within the IR, and calculate some meta information
    ir = ir | aS(p5.IR.calc) | aS(p5.IR.calcMeta)
    # create a p5 sketch, setup some initial variables
    p5.newSketch(400, 400); p5.background(155); p5.textSize(16)
    # creates an image from the IR
    IR.display(ir); im = p5.img()

The idea is, you can define the sketch however you like, with relationships between them (like how
a line is made of 2 points, or construct a circle with a specified center that passes through another
point). After that, you'll receive the IR, which is a simple object that can be turned into a json
that can be understood by other parts of your system.

After you got the IR, you can calculate the precise location of every element with :meth:`IR.calc`.
Then you can calculate extra metadata about the viewing frame to display it on with :meth:`IR.calcMeta`.
Finally, you can do :meth:`IR.display`
"""                                                                              # Entity
        self.irL = type(self).init(*args)                                        # Entity
    def __ror__(self, ir): ir = ir or {"def": {}, "meta": None}; ir["def"][self.irL[0]] = self.irL; return ir # Entity
    @classmethod                                                                 # Entity
    def dependsOn(cls,ir,name:str) -> List[str]:                                 # Entity
        """Should return List[name]]"""                                          # Entity
        return []                                                                # Entity
    @classmethod                                                                 # Entity
    def calc(cls,ir,name:str) -> List[float]: return NotImplemented              # Entity
    @classmethod                                                                 # Entity
    def bounds(cls,ir,name:str) -> List[float]: return [inf,-inf,inf,-inf] # calculates the bounds of the object: xmin, xmax, ymin, ymax # Entity
    @classmethod                                                                 # Entity
    def display(cls,ir,name:str,meta): pass # meta = [transXY (lambda), scale: (lambda)] # Entity
class Point(Entity): # final coordinate format: [x, y]                           # Point
    @classmethod                                                                 # Point
    def display(cls,ir,name):                                                    # Point
        o = ir["def"][name]; props = {**{"stroke": "#ff0000"},**(o[3] or {})}    # Point
        if props.get("display", None) == "none": return                          # Point
        if "stroke" in props: stroke(props["stroke"])                            # Point
        x,y = ir["meta"][0](*o[4]); fill(255); ellipse(x,y,3); text(props.get("name", name),x+6,y+6) # Point
    @classmethod                                                                 # Point
    def bounds(cls,ir,name): x,y = ir["def"][name][4]; return [x,x,y,y]          # Point
def point_rnd(name:str, props=None):                                             # point_rnd
    """Creates a point with a random location. See also: :class:`Entity`

:param name: name of point"""                                                    # point_rnd
    return point_raw(name, *np.random.randn(2), props)                           # point_rnd
class point_raw(Point):                                                          # point_raw
    def __init__(self,name:str,x:float,y:float,props=None):                      # point_raw
        """Creates a point from actual raw coordinates. See also: :class:`Entity`

:param name: name of point
:param x: position on x axis
:param y: position on y axis"""                                                  # point_raw
        self.irL = [name, "point_raw", [x, y], props, []]                        # point_raw
    @classmethod                                                                 # point_raw
    def dependsOn(cls,ir,name:str): return []                                    # point_raw
    @classmethod                                                                 # point_raw
    def calc(cls,ir,name:str): return ir["def"][name][2]                         # point_raw
class point_sym(Point):                                                          # point_sym
    def __init__(self,name:str,p1:str,pm:str,props=None):                        # point_sym
        """Creates a point which is symmetric to point "p1" around point "pm".
Basically, "pm" is the midpoint of "p1" and the new point. See also: :class:`Entity`

:param name: name of point
:param p1: name of the other point
:param pm: name of the middle point"""                                           # point_sym
        self.irL = [name, "point_sym", [p1,pm], props, []] # point 1 and point mid # point_sym
    @classmethod                                                                 # point_sym
    def dependsOn(cls,ir,name:str): return ir["def"][name][2]                    # point_sym
    @classmethod                                                                 # point_sym
    def calc(cls,ir,name:str): p1,pm = ir["def"][name][2]; x1,y1 = ir["def"][p1][4]; xm,ym = ir["def"][pm][4]; dx = xm-x1; dy = ym-y1; return [x1+2*dx, y1+2*dy] # point_sym
class point_L(Point):                                                            # point_L
    def __init__(self,name:str,l1:str,f:float,props=None):                       # point_L
        """Creates a point on a line at a particular fraction.
If "f" is 0.1, it'll be close to the first point of the line,
if "f" is 0.9, it'll be close to the second point of the line.

:param name: name of point
:param l1: name of line that the point is on
:param f: fraction between the 2 points on the line. Can be any number, not just from 0 to 1""" # point_L
        self.irL = [name, "point_L", [l1,f], props, []]                          # point_L
    @classmethod                                                                 # point_L
    def dependsOn(cls,ir,name:str): return ir["def"][name][2][:1]                # point_L
    @classmethod                                                                 # point_L
    def calc(cls,ir,name:str): l1,f = ir["def"][name][2]; x1,y1,x2,y2 = ir["def"][l1][4]; return x1*(1-f)+x2*f, y1*(1-f)+y2*f # point_L
def triangle(p1:str,p2:str,p3:str,props1=None,props2=None,props3=None):          # triangle
    """Creates 3 random points that looks like a reasonable triangle,
with flat base and pointy upward tip.

:param p1: name of first point
:param props1: optional properties of the first point"""                         # triangle
    while True:                                                                  # triangle
        ya, yb = np.random.randn(2)                                              # triangle
        if ya < yb: ya, yb = yb, ya                                              # triangle
        x2, x3 = np.random.randn(2)                                              # triangle
        if x2 > x3: x2,x3 = x3,x2                                                # triangle
        x1 = x2+random.random()*(x3-x2)                                          # triangle
        if 0.3 < abs(ya-yb)/abs(x3-x2) < 3: break                                # triangle
    return point_raw(p1,x1,ya,props1) | point_raw(p2,x2,yb,props2) | point_raw(p3,x3,yb,props3) # triangle
class Line(Entity): # final coordinate format: [x1, y1, x2, y2]                  # Line
    @classmethod                                                                 # Line
    def display(cls,ir,name):                                                    # Line
        o = ir["def"][name]; props = {**{"stroke": "#0000ff"},**(o[3] or {})}    # Line
        if props is not None and props.get("display", None) == "none": return    # Line
        if "stroke" in props: stroke(props["stroke"])                            # Line
        f = ir["meta"][0]; x1,y1,x2,y2 = o[4] | cli.batched(2) | ~cli.apply(f) | cli.joinSt(); line(x1,y1,x2,y2); text(props.get("name", name),(x1+x2)/2+6, (y1+y2)/2+6) # Line
    @classmethod                                                                 # Line
    def bounds(cls,ir,name): x1,y1,x2,y2 = ir["def"][name][4]; return [min(x1,x2), max(x1,x2), min(y1,y2), max(y1,y2)] # Line
class line_P(Line):                                                              # line_P
    def __init__(self,name:str,p1:str,angle:float,l:float,f:float=0.5,props=None): # line_P
        """Creates a line that passes through a point, with an angle from the x axis, a specific length and a specific point fraction.

:param name: name of line
:param p1: name of point
:param angle: angle with respect to the x axis
:param l: length of the line
:param f: fraction of the line the point is located at"""                        # line_P
        self.irL = [name, "line_P", [p1,angle,l,f], props, []]                   # line_P
    @classmethod                                                                 # line_P
    def dependsOn(cls,ir,name:str): return ir["def"][name][2][:1]                # line_P
    @classmethod                                                                 # line_P
    def calc(cls,ir,name:str): p1,angle,l,f = ir["def"][name][2]; x,y = ir["def"][p1][4]; dx = math.cos(angle)*l; dy = math.sin(angle)*l; return [x-dx*f, y-dy*f, x+dx*(1-f), y+dy*(1-f)]#return [x-dx*(1-f), y-dy*(1-f), x+dx*f, y+dy*f] # line_P
class line_2P(Line):                                                             # line_2P
    def __init__(self,name:str,p1:str,p2:str,prevF:float=0,nextF:float=0,props=None): # line_2P
        """Creates a line that connects 2 points together. See also: :class:`Entity`

:param name: name of line
:param p1: name of first point
:param p2: name of second point
:param prevF: "previous fraction". How much should the line extend past
    the first point as a fraction of the distance between p1 and p2
:param nextF: "next fraction". How much should the line extend past
    the second point as a fraction of the distance between p1 and p2
"""                                                                              # line_2P
        self.irL = [name, "line_2P", [p1, p2, prevF, nextF], props, []]          # line_2P
    @classmethod                                                                 # line_2P
    def dependsOn(cls,ir,name:str): return ir["def"][name][2][:2]                # line_2P
    @classmethod                                                                 # line_2P
    def calc(cls,ir,name:str):                                                   # line_2P
        p1, p2, prevF, nextF = ir["def"][name][2]; x1, y1 = ir["def"][p1][4]; x2, y2 = ir["def"][p2][4]; dx = x2 - x1; dy = y2 - y1 # line_2P
        return [x1-dx*prevF,y1-dy*prevF,x2+dx*nextF,y2+dy*nextF]                 # line_2P
class line_2PL(Line):                                                            # line_2PL
    def __init__(self,name:str,p1:str,p2:str,l:float,props=None):                # line_2PL
        """Creates a line that connects 2 points together that starts at the first
point and has specific length. If extended indefinitely, it will pass through the
second point, but in its normal state, it doesn't have to pass through or can
overshoot the second point. Useful for creating rays. See also: :class:`Entity`

:param name: name of the line
:param p1: name of first point
:param p2: name of second point
:param l: length of line
"""                                                                              # line_2PL
        self.irL = [name, "line_2PL", [p2,p2,l], props, []]                      # line_2PL
    @classmethod                                                                 # line_2PL
    def dependsOn(cls,ir,name:str): return ir["def"][name][2][:2]                # line_2PL
    @classmethod                                                                 # line_2PL
    def calc(cls,ir,name:str): pass                                              # line_2PL
class Circle(Entity): # final coordinate format: [x, y, r]                       # Circle
    @classmethod                                                                 # Circle
    def display(cls,ir,name):                                                    # Circle
        o = ir["def"][name]; props = {**{"stroke": "#000000"},**(o[3] or {})}    # Circle
        if props is not None and props.get("display", None) == "none": return    # Circle
        if "stroke" in props: stroke(props["stroke"])                            # Circle
        x,y,r = o[4]; x,y = ir["meta"][0](x,y); r *= ir["meta"][1]; ellipse(x,y,r*2); text(props.get("name", name),x+r*1.1,y) # Circle
    @classmethod                                                                 # Circle
    def bounds(cls,ir,name): x,y,r = ir["def"][name][4]; return [x-r,x+r,y-r,y+r] # Circle
class circle_PR(Circle): # circle from center point and radius                   # circle_PR
    def __init__(self,name:str,p1:str,radius:float,props=None):                  # circle_PR
        """Creates a circle from a center point and a radius. See also: :class:`Entity`

:param name: name of circle
:param p1: name of the center point
:param radius: radius of the circle"""                                           # circle_PR
        self.irL = [name, "circle_PR", [p1, radius], props, []]                  # circle_PR
    @classmethod                                                                 # circle_PR
    def dependsOn(cls,ir,name:str): return [ir["def"][name][2][0]]               # circle_PR
    @classmethod                                                                 # circle_PR
    def calc(cls,ir,name:str): o = ir["def"][name][2]; return [*ir["def"][o[0]][4], o[1]] # circle_PR
class circle_2P(Circle): # circle that has center pc and passes through point p2 # circle_2P
    def __init__(self,name:str,pc:str,p2:str,props=None):                        # circle_2P
        """Creates a circle from a center point that passes through another
point. See also: :class:`Entity`

:param name: name of circle
:param pc: name of the center point
:param p2: name of the second point that the circle passes through"""            # circle_2P
        self.irL = [name, "circle_2P", [pc, p2], props, []]                      # circle_2P
    @classmethod                                                                 # circle_2P
    def dependsOn(cls,ir,name:str): return ir["def"][name][2]                    # circle_2P
    @classmethod                                                                 # circle_2P
    def calc(cls,ir,name:str): pc, p2 = ir["def"][name][2]; xc, yc = ir["def"][pc][4]; x2, y2 = ir["def"][p2][4]; dx = x2-xc; dy = y2-yc; return [xc,yc,math.sqrt(dx*dx+dy*dy)] # circle_2P
class grid(Entity):                                                              # grid
    def __init__(self, name="grid-0", props=None):                               # grid
        """Adds a grid to the plot. See also: :class:`Entity`"""                 # grid
        self.irL = ["grid-0", "grid", [], props, []]                             # grid
    @classmethod                                                                 # grid
    def display(cls,ir,name):                                                    # grid
        if not ir["meta"]: raise Exception(f"Please calculate the positions of everything and metadata first, before trying to display an IR that has a grid") # grid
        o = ir["def"][name]; meta = ir["meta"]; w,h = meta[2]; [dx,dy],[cx,cy],[x,y] = meta[4:7]; f,s = meta[:2] # grid
        scale = int(math.log10(max(dx,dy)/1.3)); fac = 10**scale # 10^scale for the grid's spacing # grid
        ccx = max((w/h)/(dx/dy), 1); ccy = max((h/w)/(dy/dx), 1) # correction factors # grid
        xticks = range(math.ceil((cx-ccx*dx*0.8)/fac), math.ceil((cx+ccx*dx*0.8)/fac)) | cli.apply(cli.op()/fac) | cli.deref() # grid
        yticks = range(math.ceil((cy-ccy*dy*0.8)/fac), math.ceil((cy+ccy*dy*0.8)/fac)) | cli.apply(cli.op()/fac) | cli.deref() # grid
        with context():                                                          # grid
            stroke(100)                                                          # grid
            for x in xticks: line(*f(x, cy-ccy*dy*1.2), *f(x, cy+ccy*dy*1.2))    # grid
            for y in yticks: line(*f(cx-ccx*dx*1.2, y), *f(cx+ccx*dx*1.2, y))    # grid
def round2(x): return int(x) if int(x) == x else x                               # round2
class axes(Entity):                                                              # axes
    def __init__(self, name="axes-0", props=None):                               # axes
        """Adds xy axis to the plot. See also: :class:`Entity`"""                # axes
        self.irL = ["axes-0", "axes", [], props, []]                             # axes
    @classmethod                                                                 # axes
    def display(cls,ir,name):                                                    # axes
        if not ir["meta"]: raise Exception(f"Please calculate the positions of everything and metadata first, before trying to display an IR that has a grid") # axes
        o = ir["def"][name]; meta = ir["meta"]; w,h = meta[2]; [dx,dy],[cx,cy],[x,y] = meta[4:7]; f,s = meta[:2] # axes
        scale = int(math.log10(max(dx,dy)/1.3)); fac = 10**scale # 10^scale for the grid's spacing # axes
        ccx = max((w/h)/(dx/dy), 1); ccy = max((h/w)/(dy/dx), 1) # correction factors # axes
        line(*f(0, cy-ccy*dy*1.2), *f(0, cy+ccy*dy*1.2))                         # axes
        line(*f(cx-ccx*dx*1.2, 0), *f(cx+ccx*dx*1.2, 0))                         # axes
        xticks = range(math.ceil((cx-ccx*dx*0.8)/fac), math.ceil((cx+ccx*dx*0.8)/fac)) | cli.apply(cli.op()/fac) | cli.deref() # axes
        yticks = range(math.ceil((cy-ccy*dy*0.8)/fac), math.ceil((cy+ccy*dy*0.8)/fac)) | cli.apply(cli.op()/fac) | cli.filt("x") | cli.deref() # axes
        with context():                                                          # axes
            for x in xticks: text(f"{round2(x)}", *f(x, 0) | (cli.op()-5) + (cli.op()+10)) # axes
            for y in yticks: text(f"{round2(y)}", *f(0, y) | (cli.op()+10) + (cli.op()-5)) # axes
def vlen(dx,dy): return math.sqrt(dx*dx+dy*dy) # vector length                   # vlen
entities = [point_raw, point_sym, point_L, line_P, line_2P, line_2PL, circle_PR, circle_2P, grid, axes]; entitiesD = entities | cli.apply(lambda x: [x.__name__, x]) | cli.toDict() # vlen
class IR:                                                                        # IR
    """Intermediate representation of a whole graph"""                           # IR
    @staticmethod                                                                # IR
    def dep(ir) -> Iterator[str]: # figures out the dependency graph, returns elements to calculate position of # IR
        d = defaultdict(lambda: []); a = ir["def"].values() | cli.cut(0, 1) | cli.lookup(entitiesD, 1) | ~cli.apply(lambda name,cls: [name,cls.dependsOn(ir,name)]) | ~cli.apply(lambda x,y:[x,y,len(y)]) | cli.deref() # IR
        for x,y,z in a:                                                          # IR
            for p in y: d[p].append(x)                                           # IR
        freqs = a | cli.cut(0, 2) | cli.toDict(); stack = deque(a | cli.cut(0, 2) | ~cli.filt("x", 1) | cli.cut(0) | cli.deref()) # IR
        while len(stack) > 0:                                                    # IR
            c = stack.popleft(); yield c                                         # IR
            for child in d[c]:                                                   # IR
                freqs[child] -= 1                                                # IR
                if freqs[child] == 0: stack.append(child)                        # IR
    @staticmethod                                                                # IR
    def calc(ir): # calculates position of every element and write results back to IR # IR
        for e in IR.dep(ir): ir["def"][e][4] = entitiesD[ir["def"][e][1]].calc(ir,e) # IR
        return ir                                                                # IR
    @staticmethod                                                                # IR
    def bounds(ir): return ir["def"].values() | cli.apply(lambda e: entitiesD[e[1]].bounds(ir, e[0])) | cli.transpose() | cli.toMin() + cli.toMax() + cli.toMin() + cli.toMax() | cli.deref() # IR
    @staticmethod                                                                # IR
    def calcMeta(ir,w=400,h=400): # calculates meta transformation functions     # IR
        bounds = IR.bounds(ir)                                                   # IR
        a, b, c, d = bounds; cx = (a+b)/2; cy = (c+d)/2; dx = b-a; dy = d-c      # IR
        sx = w/dx; sy = h/dy; s = min(sx, sy)/1.2; f1 = lambda x,y: [(x-cx)*s+w/2, (y-cy)*s+h/2] # IR
        ir["meta"] = [f1, s, [w, h], [sx, sy], [dx, dy], [cx, cy], [a, c]]; return ir # IR
    @staticmethod                                                                # IR
    def display(ir,w=400,h=400): # constructs an image of the IR                 # IR
        if not ir["meta"]: IR.calcMeta(ir,w,h)                                   # IR
        # draw order: circle -> line -> point, because transparent fills are not really a thing in this knock up version of p5 # IR
        for e in ir["def"].values() | cli.filt(cli.op().split("_")[0] == "grid", 1): entitiesD[e[1]].display(ir,e[0]) # IR
        for e in ir["def"].values() | cli.filt(cli.op().split("_")[0] == "axes", 1): entitiesD[e[1]].display(ir,e[0]) # IR
        for e in ir["def"].values() | cli.filt(cli.op().split("_")[0] == "circle", 1) | ~cli.sortF(cli.op()[4][2]): entitiesD[e[1]].display(ir,e[0]) # IR
        for e in ir["def"].values() | cli.filt(cli.op().split("_")[0] == "line",   1): entitiesD[e[1]].display(ir,e[0]) # IR
        for e in ir["def"].values() | cli.filt(cli.op().split("_")[0] == "point",  1): entitiesD[e[1]].display(ir,e[0]) # IR
    @staticmethod                                                                # IR
    def dist_2P(ir, o1:str, o2:str):                                             # IR
        """Calculates distance between 2 objects given their names"""            # IR
        o1 = ir["def"][o1]; o2 = ir["def"][o2]; x1,y1 = o1[4]; x2,y2 = o2[4]; return vlen(x2-x1, y2-y1) # IR
    @staticmethod                                                                # IR
    def length_L(ir, line:str):                                                  # IR
        """Calculates the length of a specific line"""                           # IR
        x1,y1,x2,y2 = ir["def"][line][4]; return vlen(x2-x1, y2-y1)              # IR
    @staticmethod                                                                # IR
    def angle_2L(ir, l1:str, l2:str) -> "``radians``":                           # IR
        """Calculates the angle between 2 lines"""                               # IR
        x1,y1,x2,y2 = ir["def"][l1][4]; x3,y3,x4,y4 = ir["def"][l2][4]           # IR
        dx1 = x2-x1; dx2 = x4-x3; dy1 = y2-y1; dy2 = y4-y3                       # IR
        return math.acos((dx1*dx2+dy1*dy2)/vlen(dx1,dy1)/vlen(dx2,dy2))          # IR
k1lib.settings.add("p5", k1lib.Settings()                                        # IR
    .add("funcs", ["arc", "ellipse", "circle", "line", "point", "quad", "rect", "square", "triangle", "text", # IR
                   "color", "fill", "noFill", "stroke", "noStroke", "background"], "p5 functions to syntactically replace in instance mode") # IR
    .add("symbols", ["mouseX", "mouseY"], "symbols to syntactically replace in instance mode"), # IR
"p5 module settings");                                                           # IR
class Sketch(cli.BaseCli):                                                       # Sketch
    def __init__(self, f:str, width=500, height=500):                            # Sketch
        """Creates a real p5js sketch, but make it convenient.
Example::

    "some data" | p5.Sketch('''
        function setup() {
            background(200);
        }
        function draw() {
            background(200);
            text(data, 20, 20);
            ellipse(mouseX, mouseY, 20, 20);
        }
    ''')

:param f: the js string to inject into the sketch
:param width: width of the sketch
:param height: height of the sketch"""                                           # Sketch
        self.width = width; self.height = height                                 # Sketch
        if "function setup() {" not in f: raise Exception("Function setup() not found, please start the function with `function setup() {`") # Sketch
        if "function draw() {" not in f:  raise Exception("Function draw() not found, please start the function with `function draw() {`") # Sketch
        self.f = f.replace("function setup() {", f"function setup() {{ p.createCanvas({width}, {height}); ") # Sketch
    def __ror__(self, it):                                                       # Sketch
        pre = cli.init._jsDAuto(); f = self.f                                    # Sketch
        for sym in k1lib.settings.p5.funcs:   f = f.replace(f"{sym}(", f"p.{sym}(") # Sketch
        for sym in k1lib.settings.p5.symbols: f = f.replace(f"{sym}", f"p.{sym}") # Sketch
        f = f.replace(".p.", ".")                                                # Sketch
        return k1lib.viz.Html(f"""
<div id="{pre}_sketch" style="width: {self.width}px; height: {self.height}px"></div>
<div id="{pre}_errors">&nbsp;</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.3/p5.min.js" integrity="sha512-0zGLOFv/+OQ6YfVCSGDQWhrDRx0ONmBqWvs3gI4olm8i6xtKoG1FhEnB4eTaWCVnojyfUDgE8Izeln+mAJAkFA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script>
    new p5(p => {{
        const data = {json.dumps(it)};{f}
        p.setup = setup;
        p.draw = draw;
    }}, document.querySelector("#{pre}_sketch"));
</script>
""")                                                                             # Sketch
class Anim(cli.BaseCli):                                                         # Anim
    def __init__(self, width=500, height=500):                                   # Anim
        """Creates a quick animation that internally runs on p5js.
Why not just use matplotlib or smth? Their performance is quite
terrible, and sometimes I just want a simple way to display
animations. Example::

    [[0,    "ellipse(200,300,20,20);text('abc',20,20);"],
     [0.03, "ellipse(204,299,19,19);text('abc',22,23);"]] | p5.Anim()

The left column is the time in seconds to draw the frame, and the right column is the
code to execute on that frame. Pretty simple really."""                          # Anim
        self.width = width;                                                      # Anim
        self.height = height                                                     # Anim
    def __ror__(self, it):                                                       # Anim
        pre = cli.init._jsDAuto(); it = it | cli.sort() | cli.deref(); maxT = it[-1][0] # Anim
        timeouts = it | ~cli.apply(lambda x,y: f"setTimeout(() => {{ background(200);text('Time: {x}s, {round(x/maxT*100,2)}%',20,{self.height-20});{y} }}, {x*1000});") | cli.join("\n") # Anim
        return None | Sketch(f"""
{pre}_refresh = () => {{ {timeouts}; }}; {pre}_refresh();
setInterval({pre}_refresh, {(maxT+1)*1000});
function setup() {{ background(200); }}
function draw() {{ }}
""", self.width, self.height)                                                    # Anim
