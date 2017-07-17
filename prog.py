import serial
import sys
from serial.tools.list_ports import comports
from time import sleep


get_seti = "ISET1?"
get_i = "IOUT1?"
get_setv = "VSET1?"
get_v = "VOUT1?"
get_stat = "STATUS?"
get_id = "*IDN?"
set_off = "OUTPUT0"
set_on = "OUTPUT1"
set_i = "ISET1:"
set_v = "VSET1:"
ser = serial.serial_for_url('/dev/ttyUSB1', 9600, timeout=1)


def send(command):
    command = ("%s\\r\\n" % (command)).encode()
    ser.write(command)
    #print(command)
    sleep(0.3)
    return ser.read(ser.in_waiting).strip(b'\n').decode('ascii')


def status():
    print("STATUS: %s" % (send(get_stat)))
    print("SET I: %s" % (send(get_seti)))
    print("SET V: %s" % (send(get_setv)))
    print("VALUE I: %s" % (send(get_i)))
    print("VALUE V: %s\n" % (send(get_v)))


def main():
    ports = []
    print("ID: %s" % (send(get_id)))
    i = "0.000"
    v = "00.00"
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        sys.stderr.write('--- {:2}: {:20} {}\n'.format(n, port, desc))
        ports.append(port)
    status()
    i = "1.000"
    v = "05.00"
    print("SET I: %s" % (i))
    send("%s%s" % (set_i, i))
    status()
    print("SET V: %s" % (v))
    send("%s%s" % (set_v, v))
    status()
    print("ENABLE")
    send(set_on)
    sleep(2)
    status()
    i = "0.000"
    v = "00.00"
    print("SET I: %s" % (i))
    send("%s%s" % (set_i, i))
    print("SET V: %s" % (v))
    send("%s%s" % (set_v, v))
    status()
    print("DISABLE")
    send(set_off)
    sleep(2)
    status()
    ser.close()

if __name__ == '__main__':
    main()

