#!/usr/bin/env python
import socket
import sys
import motors
import random


def log(sock, msg):
    sock_message = msg.encode()
    sock.send(sock_message)
    print(sock_message.msg())

# socket settings
TCP_IP = '0.0.0.0'
TCP_PORT = 25555
BUFFER_SIZE = 16
packet_size = 4

print("Python version: " + sys.version)

# create and ready our socket with its settings
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Awaiting connection...")
conn, addr = s.accept()
print("Connection address: ", addr)
while 1:
    try:
        data = conn.recv(BUFFER_SIZE)
    except:
        print("Client disconnected. Awaiting connection...")
        conn, addr = s.accept()  # wait here until a new connection.
        print("Connection address: ", addr)
        continue

    # if a dash character is received, immediately quit the application
    if data == '-':
        break

    # print what we received
    print("Received: ", data)

    # decode the data so we can work with it
    data = data.decode()

    try:
        # parse received data
        if data[0] == '^':  # FWD
            data = data[2:]
            if data and isinstance(int(data), int) and 0 < int(data) <= 5:
                log(conn, motors.go_fwd(int(data)))
            elif data == 0:
                log(conn, motors.halt_motors())
            else:
                data = ''
                log(conn, motors.go_fwd(data))

        elif data[0] == 'v':  # BWD
            data = data[2:]
            if data and isinstance(int(data), int) and 0 > int(data) >= -5:
                log(conn, motors.go_bwd(int(data)))
            elif data == 0:
                log(conn, motors.halt_motors())
            else:
                data = ''
                log(conn, motors.go_bwd(data))

        elif data[0] == '*':  # STOP
            log(conn, motors.halt_motors())
        elif data[0] == 'b':  # BATTERY Request
            log(conn, "BATT " + str(random.randint(1, 100)))
        elif data[0] == 's':  # WIFI SIGNAL STRENGTH Request
            log(conn, "SIG: 100%")
        else:
            # noinspection PyTypeChecker
            log(conn, " -Error: unimplemented command.")
    except:
        log(conn, "Problem parsing data: " + data)
        continue

print("Terminating..." + str(1))
conn.close()
