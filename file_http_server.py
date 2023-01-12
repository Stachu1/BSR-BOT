import socket
from flask import Flask, send_file
app = Flask(__name__)

@app.route('/mp3')
def downloadFile_yt_mp3():
    path = "converted.mp3"
    return send_file(path, as_attachment=True)

@app.route('/mp4')
def downloadFile_yt_mp4():
    path = "converted.mp4"
    return send_file(path, as_attachment=True)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 0))
port = sock.getsockname()[1]
sock.close()

port = 5555
print("port:", port)

app.run(host="0.0.0.0", port=port, debug=False)