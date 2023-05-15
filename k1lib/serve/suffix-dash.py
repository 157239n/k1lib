import os
{"type": "dashapp", "pid": os.getpid()} | aS(dill.dumps) | file("META_FILE")

app = dashApp()
app.run('0.0.0.0', debug=True, port=SOCKET_PORT)
