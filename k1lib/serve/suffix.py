import inspect, io, base64
from flask import Flask, request
from flask_cors import CORS

goodTypes = (int, float, str, bool, bytes, PIL.Image.Image, k1.Range, range, list)

spec = inspect.getfullargspec(endpoint); args = spec.args; annos = spec.annotations; defaults = spec.defaults or (); n = len(args)
docs = (endpoint.__doc__ or "").split("\n") | grep(":param", sep=True).till() | filt(op().ab_len() > 0) | op().strip().all(2) | (join(" ") | op().split(":") | ~aS(lambda x, y, *z: [y.split(" ")[1], ":".join(z).strip()])).all() | toDict()
mainDoc = (endpoint.__doc__ or "").split("\n") | grep(".", sep=True).till(":param") | breakIf(op()[0].startswith(":param")) | join(" ").all() | join(" ")

def raiseEx(ex): raise ex
if len(annos) != n + 1: raise Exception(f"Please annotate all of your arguments ({n} args + 1 return != {len(annos)} annos). Args: {args}, annos: {annos}")
if len(defaults) != n: raise Exception(f"Please specify default values for all of your arguments ({n} args != {len(defaults)} default values)")
if not annos.values() | apply(lambda x: x in goodTypes) | aS(all): raise Exception(f"Some of your types: {annos | ~inSet(goodTypes) | deref()} are not supported by the system. Please only use these types: {goodTypes}")
if annos["return"] in (k1.Range, range): raise Exception(f"Return value is {annos['return']}, which doesn't really make sense")
defaults = defaults | apply(lambda x: [x.start, x.stop] if isinstance(x, k1.Range) else x)\
    | apply(lambda x: [x.start, x.stop, x.step] if isinstance(x, range) else x)\
    | apply(lambda x: x | aS(base64.b64encode) | op().decode("ascii") if isinstance(x, bytes) else x)\
    | apply(lambda x: x | toBytes() | aS(base64.b64encode) | op().decode("ascii") if isinstance(x, PIL.Image.Image) else x)\
    | apply(lambda x: x | apply(str) if isinstance(x, list) else x) | deref()
defaults = [args, defaults] | toDict(False)

# args:list, annos:dict, defaults:list, docs:dict

{"args": args, "annos": annos, "defaults": defaults, "docs": docs,
 "mainDoc": mainDoc, "source": inspect.getsource(endpoint), "pid": os.getpid(),
 "goodTypes": goodTypes} | aS(dill.dumps) | file("META_FILE")

def webToPy(o:str, klass):
    o = str(o)
    if klass == int: return int(o)
    if klass == float: return float(o)
    if klass == str: return o
    if klass == bool: return o.lower() == "true"
    if klass == bytes: return o | aS(base64.b64decode)
    if klass == PIL.Image.Image: return o | aS(base64.b64decode) | toImg()
    if klass == k1.Range: return float(o)
    if klass == range: return int(o)
    if klass == list: return o
    return NotImplemented

def pyToWeb(o, klass):
    if klass in (int, float, str, bool): return f"{o}"
    if klass in (k1.Range, range): return NotImplemented
    if klass == bytes: return o | aS(base64.b64encode)
    if klass == PIL.Image.Image: return o | toBytes() | aS(base64.b64encode)
    if klass == list: return o;
    return NotImplemented

app = Flask(__name__); CORS(app)

@app.route("/healthCheck", methods=["GET", "POST"])
def healthCheck():
    return "ok"

@app.route("/", methods=["POST"])
def main():
    js = request.json
    return pyToWeb(endpoint(*[webToPy(js[arg], annos[arg]) for arg in args]), annos["return"])

try:
    import waitress
    waitress.serve(app, host='0.0.0.0', port=SOCKET_PORT)
except: app.run(host='0.0.0.0', port=SOCKET_PORT)



