import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

groups = {}

while True:
    try:
        message = socket.recv_json()
        if message['action'] == 'register':
            groups[message['name']] = message['address']
            print(f"JOIN REQUEST FROM {message['address']}")
            socket.send_json({"status": "SUCCESS"})
        elif message['action'] == 'get_groups':
            print(f"GROUP LIST REQUEST FROM {message['client_address']}")
            socket.send_json(groups)
    except Exception as e:
        print(f"An error occurred: {e}")
