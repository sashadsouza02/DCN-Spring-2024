from flask import Flask, abort, request
import json
import socket

app = Flask(__name__)

@app.route('/fibonacci')
def fiboseries():
    n = request.args.get('n', default=1, type=int)
    fibo = [1, 1]
    for i in range(2, n):
        fibo.append(fibo[i-1] + fibo[i-2])
    return str(fibo[:n])

requestdict = {"hostname": "", "ip": "", "as_ip": "", "as_port": ""}

@app.route('/register', methods=["PUT", "GET"])
def register():
    if request.method in ["GET", "PUT"]:
        try:
            input_string = request.get_json(force=True)
            requestdict["hostname"] = str(input_string["hostname"])
            requestdict["ip"] = str(input_string["ip"])
            requestdict["as_ip"] = str(input_string["as_ip"])
            requestdict["as_port"] = str(input_string["as_port"])
            print(requestdict)
            response = registerFSonAS()
            return response
        except Exception as e:
            print(e)
            abort(400)
    else:
        abort(405)  # Method Not Allowed

def registerFSonAS():
    as_ip = requestdict["as_ip"]
    as_port = int(requestdict["as_port"])
    server_address = (as_ip, as_port)
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
        message = generatedmessage()
        sock.sendto(message.encode(), server_address)
        # Assuming the AS responds immediately; otherwise, you might not need to wait for a response here
        responsefromserver, _ = sock.recvfrom(1024)
        print(responsefromserver)
        return "Registration sent to AS."

def generatedmessage():
    message = f"TYPE=A\nNAME={requestdict['hostname']}\nVALUE={requestdict['ip']}\nTTL=10"
    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
