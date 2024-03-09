# ZeroMQ Message System

This project implements a simple message system using ZeroMQ with three components: `message_server`, `groups`, and `user`. The system allows users to register, join and leave groups, send and receive messages within groups.

## Overview

The project consists of three main components:

1. **message_server.py:**
   - Acts as a central server for handling group registrations and managing group addresses.
   - Provides an interface for users to register and request a list of available groups.

2. **groups.py:**
   - Represents the group server, allowing users to join, leave, send, and receive messages within a group.
   - Registers with the central message server for group management.

3. **user.py:**
   - Simulates a user client that can interact with the message system.
   - Allows users to join groups, send messages, and receive messages from the current group.

## Setup

### Prerequisites
- Python installed on your system.
- ZeroMQ library installed.

### Steps

1. **Install Dependencies:**
   - Ensure Python and ZeroMQ are installed on your system.

2. **Run `message_server.py`:**
   - Execute the `message_server.py` script to start the central message server.
   - Provide the IP address and port where the server should bind (e.g., `0.0.0.0:5555`).

3. **Run `groups.py`:**
   - Execute the `groups.py` script to start a group server.
   - Enter the IP address of the message server when prompted.
   - Enter the IP address and port for the group server.

4. **Run `user.py`:**
   - Execute the `user.py` script to simulate a user interacting with the system.
   - Enter the IP address of the message server when prompted.
   - Enter the user's address (IP:Port).

## Usage

- Upon running `user.py`, the user can:
  - Get a list of available groups.
  - Join a group by providing the group's address.
  - Leave the current group.
  - Send a message to the current group.
  - Receive messages from the current group.

## Notes

- All components must be running for the system to function correctly.
- Ensure proper network connectivity and firewall settings for communication between components.
- Use the provided IP addresses and ports as per your network configuration.

Feel free to explore and customize the system based on your requirements!
