from flask import Flask, request, jsonify, abort
import socket
import json
import requests

app = Flask(__name__)

def validate_run(hostname, fs_port, num, as_ip, as_port):
    if not all([hostname, fs_port, num, as_ip, as_port]):
        abort(400, "All parameters are required.")

def fibo_url(ip, num):
    url = f"http://{ip}:9090/fibonacci?number={num}"
    return url

def dns_query(hostname):
    return f"NAME={hostname}\nTYPE=A"

def query_ip_from_as(hostname, as_ip, as_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_us:
        dns_query_str = dns_query(hostname)
        server = (as_ip, int(as_port))
        socket_us.sendto(dns_query_str.encode(), server)
        response, _ = socket_us.recvfrom(1024)
        return json.loads(response.decode())

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    validate_run(hostname, fs_port, number, as_ip, as_port)

    response = query_ip_from_as(hostname, as_ip, as_port)

    if 'VALUE' not in response:
        abort(500, "Invalid response from AS.")

    fibonacci_ip = response['VALUE']
    fibonacci_query_url = fibo_url(fibonacci_ip, number)
    result = requests.get(fibonacci_query_url)

    if result.status_code == 200:
        return jsonify(result.json())
    else:
        abort(result.status_code, "Failed to retrieve Fibonacci sequence.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
