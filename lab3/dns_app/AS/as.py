from flask import abort
import socket
import json

UDP_IP = "0.0.0.0"
UDP_PORT = 53533
FILE = "register_info.json"

socket_as = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_as.bind((UDP_IP, UDP_PORT))

def get_dictionary(input_data):
    entries = {}
    for element in input_data.split("\n"):
        key, value = element.split("=", 1)  
        entries[key] = value
    return entries

def update_entry(data):
    try:
        with open(FILE, 'r') as file:
            register_data = json.load(file)
    except FileNotFoundError:
        print("File not found. Creating a new registry.")
        register_data = {}

    register_data[data['NAME']] = {
        "TYPE": data['TYPE'],
        "VALUE": data['VALUE'],
        "TTL": int(data['TTL'])
    }

    print(f"DATA: {register_data}")
    try:
        with open(FILE, "w") as file:
            json.dump(register_data, file, indent=4)
        print("Entry registered successfully.")
    except Exception as e:
        print(f"Error while registering hostname: {e}")

def result_query(data):
    try:
        with open(FILE) as file:
            entry = json.load(file)
    except FileNotFoundError:
        print("Unable to open file.")
        abort(400)

    hostname = next((line.split("=")[1] for line in data.split("\n") if line.startswith("NAME")), None)
    if hostname and hostname in entry:
        return {key: entry[hostname][key] for key in ['NAME', 'TYPE', 'VALUE', 'TTL']}
    else:
        print("Hostname not found in registry.")
        return {}

while True:
    print(f"Listening: {UDP_IP} {UDP_PORT}")
    data, addr = socket_as.recvfrom(1024)
    print(f"Received message: {data}")
    data = data.decode('utf-8')
    
    if data.startswith('#'):
        print("Processing DNS QUERY")
        result = result_query(data[1:])
        print(f"QUERY RESULT: {result}")
        socket_as.sendto(json.dumps(result).encode(), addr)
    else:
        data_dict = get_dictionary(data)
        update_entry(data_dict)
        print("Entry created/updated.")
        socket_as.sendto(b"success:201", addr)
