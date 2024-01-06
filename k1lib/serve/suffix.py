import inspect, io, base64, traceback
from flask import Flask, request
from flask_cors import CORS

_serve_d = k1lib.serve.analyze(endpoint); _serve_args = _serve_d["args"]; _serve_annos = _serve_d["annos"]; _serve_privates = _serve_d["privates"]
del _serve_d["privates"]; _serve_d | aS(dill.dumps) | file("META_FILE")
_serve_app = Flask(__name__); CORS(_serve_app)

@_serve_app.route("/healthCheck", methods=["GET", "POST"])
def _serve_healthCheck(): return "ok"

@_serve_app.route("/", methods=["POST"])
def _serve_main():
    try:
        js = request.json
        for arg in [arg for arg in _serve_args if _serve_annos[arg] == "apiKey"]: # if has serve.apiKey(), then check if the key matches. If not, then raise exception
            if js[arg] != _serve_privates[arg]: raise Exception(f"Api key '{arg}' wrong or is not specified")
        return {"data": k1lib.serve.pyToWeb(endpoint(*[k1lib.serve.webToPy(js[arg], _serve_annos[arg]) for arg in _serve_args]), _serve_annos["return"]), "success": True}
    except Exception as e: return {"data": None, "success": False, "reason": f"Error encountered: {e}\n\n{traceback.format_exc()}"}

try:
    import waitress
    waitress.serve(_serve_app, host='0.0.0.0', port=SOCKET_PORT)
except: _serve_app.run(host='0.0.0.0', port=SOCKET_PORT)



