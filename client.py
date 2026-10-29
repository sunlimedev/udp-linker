# Client file for UDP discovery.
# Used by Raspberry Pi client.


# ------------------ imports -------------------------------------------------------------------------------------------


import socket
import subprocess

from time import sleep


# ------------------ constants -----------------------------------------------------------------------------------------


UDP_PORT = 12321

BROADCAST_ADDRESS = "255.255.255.255"

CLIENT_PAYLOAD = b"WHO IS THE SERVER"

SERVER_PAYLOAD = b"I AM THE SERVER"

RETRY_INTERVAL = 2

RESPONSE_TIMEOUT = 1


# ------------------ socket --------------------------------------------------------------------------------------------


# set socket protocol as UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# enable sending UDP broadcast packets
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# wait a bit for a response instead of blocking indefinitely
sock.settimeout(RESPONSE_TIMEOUT)


# ------------------ kiosk ---------------------------------------------------------------------------------------------


def open_kiosk(ip_address: str):
    # open chromium in kiosk mode at given IP
    cmd = [
        "chromium",
        "--kiosk",
        "--noerrdialogs",
        "--disable-infobars",
        "--no-first-run",
         f"https://{ip_address}/"
    ]
    subprocess.run(cmd)


# ------------------ loop ----------------------------------------------------------------------------------------------


while True:
    # send a discovery request to the local network broadcast address
    sock.sendto(CLIENT_PAYLOAD, (BROADCAST_ADDRESS, UDP_PORT))

    try:
        while True:
            payload, addr = sock.recvfrom(len(SERVER_PAYLOAD))

            # run chromium kiosk mode if payload is good
            if payload == SERVER_PAYLOAD:
                print(f"Server found at {addr[0]}:{addr[1]}")
                open_kiosk(addr[0])
                break
    except socket.timeout:
        print("No server found; retrying.")

    sleep(RETRY_INTERVAL)