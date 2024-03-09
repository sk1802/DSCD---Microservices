import zmq
import json
import threading
from datetime import datetime

class GroupServer:
    def __init__(self, name, address, message_server_address):
        self.name = name
        self.address = address
        self.users = {}  # Using a dictionary to map user UUIDs to their addresses
        self.messages = []  # List of tuples (timestamp, user UUID, message)

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind(f"0.0.0.0:{address.split(':')[-1]}")

        self.register_with_message_server(message_server_address)

    def register_with_message_server(self, message_server_address):
        try:
            req_socket = self.context.socket(zmq.REQ)
            req_socket.connect(message_server_address)
            req_socket.send_json({"action": "register", "name": self.name, "address": self.address})
            response = req_socket.recv_json()
            print(response['status'])
        except Exception as e:
            print(f"Error registering with message server: {e}")

    def handle_request(self, client_id, request):
        action = request.get('action')
        if action == 'joinGroup':
            self.users[request['uuid']] = client_id
            response = {"status": "SUCCESS"}
            print(f"JOIN REQUEST FROM {request['uuid']}")
        elif action == 'leaveGroup':
            if request['uuid'] in self.users:
                del self.users[request['uuid']]
                response = {"status": "SUCCESS"}
            else:
                response = {"status": "FAIL", "reason": "User not in group"}
            print(f"LEAVE REQUEST FROM {request['uuid']}")
        elif action == 'sendMessage':
            if request['uuid'] in self.users:
                timestamp = datetime.now().timestamp()
                self.messages.append((timestamp, request['uuid'], request['message']))
                response = {"status": "SUCCESS"}
                print(f"MESSAGE SEND FROM {request['uuid']}")
            else:
                response = {"status": "FAIL"}
        elif action == 'getMessage':
            if request['uuid'] in self.users:
                timestamp = request.get('timestamp', 0)
                filtered_messages = [msg for msg in self.messages if msg[0] > timestamp]
                response = filtered_messages
                print(f"MESSAGE REQUEST FROM {request['uuid']}")
            else:
                response = {"status": "FAIL", "reason": "User not in group"}
        else:
            response = {"status": "FAIL", "reason": "Invalid action"}
        
        self.socket.send_multipart([client_id, b'', json.dumps(response).encode()])

    def start(self):
        try:
            while True:
                client_id, _, request = self.socket.recv_multipart()
                request = json.loads(request.decode())
                threading.Thread(target=self.handle_request, args=(client_id, request)).start()
        except KeyboardInterrupt:
            print("Terminating GroupServer.")
            self.socket.close()

if __name__ == "__main__":
    ip_addr_message_server = input("Enter the IP address of the messege server: ")  # Replace with the IP address of the message server
    message_address = f"tcp://{ip_addr_message_server}:5555"
    ip_addr_message = input("Enter the IP address of the group ")
    ip_port = input("Enter the port of the group server: ")
    group_server = GroupServer("GroupName", f"tcp://{ip_addr_message}:{ip_port}", f"tcp://{ip_addr_message_server}:5555")
    group_server.start()
