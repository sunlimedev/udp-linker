# Server file for UDP discovery.
# Used by Debian server.


# ------------------ imports -------------------------------------------------------------------------------------------


import socket


# ------------------ constants -----------------------------------------------------------------------------------------


HOST_ADDRESS = "0.0.0.0"

UDP_PORT = 12321

CLIENT_PAYLOAD = b"WHO IS THE SERVER"

SERVER_PAYLOAD = b"I AM THE SERVER"


# ------------------ socket --------------------------------------------------------------------------------------------


# set socket protocol as UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# allow the OS to reuse this address after a program restart
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# listen on all IPv4 network interfaces
sock.bind((HOST_ADDRESS, UDP_PORT))


# ------------------ loop ----------------------------------------------------------------------------------------------


print(f"Listening on {HOST_ADDRESS}:{UDP_PORT}")

while True:
    try:
        payload, addr = sock.recvfrom(len(CLIENT_PAYLOAD))
    except OSError as error:
        print(f"Error while receiving data: {error}")
        continue

    # respond only to valid discovery requests
    if payload == CLIENT_PAYLOAD:
        sock.sendto(SERVER_PAYLOAD, addr)
        print(f"Responded to discovery request from {addr[0]}:{addr[1]}")
