import inspect, io, base64
from flask import Flask, request
from flask_cors import CORS

d = k1lib.serve.analyze(endpoint); args = d["args"]; annos = d["annos"]
d | aS(dill.dumps) | file("META_FILE")
app = Flask(__name__); CORS(app)

@app.route("/healthCheck", methods=["GET", "POST"])
def healthCheck(): return "ok"

@app.route("/", methods=["POST"])
def main():
    js = request.json
    return k1lib.serve.pyToWeb(endpoint(*[k1lib.serve.webToPy(js[arg], annos[arg]) for arg in args]), annos["return"])

try:
    import waitress
    waitress.serve(app, host='0.0.0.0', port=SOCKET_PORT)
except: app.run(host='0.0.0.0', port=SOCKET_PORT)



