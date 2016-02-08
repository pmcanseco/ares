#!/usr/bin/env python
import socket
import sys
import motors
import serialread
import RPi.GPIO as GPIO


def log(sock, msg):
    sock_message = msg.encode()
    sock.send(sock_message)
    print(sock_message)


# socket settings
TCP_IP = '0.0.0.0'
TCP_PORT = 25555
BUFFER_SIZE = 16
packet_size = 4

print("Python version: " + sys.version)
GPIO.setmode(GPIO.BOARD)  # Use board pin numbering
GPIO.setup(7, GPIO.OUT)  # Setup GPIO Pin 7 to OUT
GPIO.output(7, True)  # Turn on GPIO pin 7
# pin 7 is the fourth one down from the right.

# create and ready our socket with its settings
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Awaiting connection...")

conn, addr = s.accept()
print("Connection address: ", addr)
GPIO.output(7, False)  # Turn off GPIO pin 7
while 1:
    try:
        data = conn.recv(BUFFER_SIZE)
    except:
        print("Client disconnected. Awaiting connection...")
        GPIO.output(7, True)  # Turn on GPIO pin 7
        conn, addr = s.accept()  # wait here until a new connection.
        print("Connection address: ", addr)
        GPIO.output(7, False)  # Turn off GPIO pin 7
        continue

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
            if data and isinstance(int(data), int) and 0 < int(data) <= 5:
                log(conn, motors.go_bwd(int(data)))
            elif data == 0:
                log(conn, motors.halt_motors())
            else:
                data = ''
                log(conn, motors.go_bwd(data))

        elif data[0] == '*':  # STOP
            log(conn, motors.halt_motors())
        elif data[0] == 'u':  # RAISE BOT
            log(conn, motors.raise_bot())
        elif data[0] == 't':  # LOWER BOT
            log(conn, motors.lower_bot())
        elif data[0] == 'y':  # STOP ACTUATORS
            log(conn, motors.stop_actuators())
        elif data[0] == 'p':  # MINE FRONT DRUM
            log(conn, motors.mine_f())
        elif data[0] == 'o':  # MINE REAR DRUM
            log(conn, motors.mine_r())
        elif data[0] == 'l':  # DUMP FRONT DRUM
            log(conn, motors.dump_f())
        elif data[0] == 'k':  # DUMP REAR DRUM
            log(conn, motors.dump_r())
        elif data[0] == 'z':  # RAISE FRONT DRUM
            log(conn, motors.raise_f())
        elif data[0] == 'x':  # LOWER FRONT DRUM
            log(conn, motors.lower_f())
        elif data[0] == 'c':  # RAISE REAR DRUM
            log(conn, motors.raise_r())
        elif data[0] == 'v':  # LOWER REAR DRUM
            log(conn, motors.lower_r())
        elif data[0] == 'b':  # BATTERY Request
            log(conn, serialread.readbatt())
        elif data[0] == 's':  # WIFI SIGNAL STRENGTH Request
            log(conn, "SIG: 100%")
        elif data[0] == '-':  # QUIT Server gracefully
            break
        else:
            log(conn, " -Error: unimplemented command.")
    except Exception as e:
        log(conn, "Problem parsing data: " + str(e) + " ...data: " + data)
        continue

print("Terminating..." + str(1))
conn.close()
motors.sp.close()
