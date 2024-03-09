import zmq
import json
from datetime import datetime
import uuid

class UserClient:
    def __init__(self, message_server_address,address):
        self.context = zmq.Context()
        self.server_socket = self.context.socket(zmq.REQ)
        self.server_socket.connect(message_server_address)
        self.group_socket = None
        self.is_joined = False
        self.group_address = ""  # Store the current group address
        self.uuid = str(uuid.uuid4())  # Generate a random UUID for the user
        self.address = address

    def get_group_list(self):
        self.server_socket.send_json({"action": "get_groups", "client_address": self.address})
        groups = self.server_socket.recv_json()
        print("Available groups:")
        for name, address in groups.items():
            print(f"{name} - {address}")

    def join_group(self, group_address):
        if self.group_socket is not None:
            self.group_socket.close()
        self.group_socket = self.context.socket(zmq.REQ)
        self.group_socket.connect(group_address)
        self.group_socket.send_json({"action": "joinGroup", "uuid": self.uuid})
        response = self.group_socket.recv_json()
        print(response['status'])
        if response['status'] == "SUCCESS":
            self.is_joined = True

    def leave_group(self):
        if self.group_socket and self.is_joined:
            self.group_socket.send_json({"action": "leaveGroup", "uuid": self.uuid})
            response = self.group_socket.recv_json()
            print(response['status'])
            self.is_joined = False
        else:
            print("You must join a group before leaving.")

    def send_message(self, message):
        if self.group_socket and self.is_joined:
            self.group_socket.send_json({"action": "sendMessage", "uuid": self.uuid, "message": message})
            response = self.group_socket.recv_json()
            print(response['status'])
        else:
            print("You must join a group before sending messages.")

    def get_messages(self, timestamp_str=""):
        if self.group_socket and self.is_joined:
            # Convert HH:MM:SS format to epoch timestamp for querying
            if timestamp_str:
                try:
                    # Convert HH:MM:SS to a datetime object for today
                    dt_obj = datetime.strptime(timestamp_str, "%H:%M:%S")
                    # Combine today's date with the input time
                    now = datetime.now()
                    combined_dt = datetime(now.year, now.month, now.day, dt_obj.hour, dt_obj.minute, dt_obj.second)
                    # Convert to epoch timestamp
                    epoch_timestamp = combined_dt.timestamp()
                except ValueError as e:
                    print("Invalid timestamp format. Please use 'HH:MM:SS'.")
                    return
            else:
                epoch_timestamp = 0  # Default to start if no timestamp is provided

            self.group_socket.send_json({"action": "getMessage", "uuid": self.uuid, "timestamp": epoch_timestamp})
            messages = self.group_socket.recv_json()
            print("Messages:")
            for msg in messages:
                # Assuming msg[0] is the epoch timestamp of the message
                # Convert epoch timestamp to 'HH:MM:SS' before printing
                time_str = datetime.fromtimestamp(msg[0]).strftime('%H:%M:%S')
                print(f"{time_str} - {msg[2]}")
        else:
            print("You must join a group to get messages.")         
               
    def menu(self):
        while True:
            print("\nAvailable actions:")
            print("1. Get list of groups")
            print("2. Join a group")
            print("3. Leave the current group")
            print("4. Send a message")
            print("5. Get messages")
            print("6. Exit")
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                self.get_group_list()
            elif choice == '2':
                if self.is_joined:
                    print("You're already in a group. Please leave the current group first.")
                else:
                    group_address = input("Enter the group address to join (e.g., tcp://localhost:6000): ")
                    self.join_group(group_address)
                    self.group_address = group_address  # Update current group address
            elif choice == '3':
                self.leave_group()
                self.group_address = ""  # Clear current group address
            elif choice == '4':
                if not self.is_joined:
                    print("You must join a group before sending messages.")
                else:
                    message = input("Enter your message: ")
                    self.send_message(message)
            elif choice == '5':
                if not self.is_joined:
                    print("You must join a group to get messages.")
                else:
                    timestamp = input("Enter the timestamp to fetch messages from in HH:MM:SS format (leave blank for all messages): ")
                    self.get_messages(timestamp)

            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    ip_msg_addr = input("Enter the IP address of the message server: ")
    message_server_address = f"tcp://{ip_msg_addr}:5555"
    user_address = input("Enter the user address [ip:port] ")
    user = UserClient(message_server_address,f"tcp://{user_address}")
    user.menu()
