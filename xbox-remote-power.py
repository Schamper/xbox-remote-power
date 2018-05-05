import sys, socket, select, time
from argparse import ArgumentParser

XBOX_PORT = 5050
XBOX_PING = "dd00000a000000000000000400000002"

py3 = sys.version_info[0] > 2


def main():
    parser = ArgumentParser(description="Send power on packets to a Xbox One.")
    parser.add_argument('-a', '--address', dest='ip_addr', help="IP Address of Xbox One", default='')
    parser.add_argument('-i', '--id', dest='live_id', help="Live ID of Xbox One", default='')
    parser.add_argument('-f', dest='forever', help="Send packets until Xbox is on", action='store_true')
    parser.add_argument('-p', '--pingonly', dest='pingonly', help="Send ping to Xbox One without turning on", action='store_true')
    args = parser.parse_args()
        
    if not args.ip_addr:
        args.ip_addr = user_input("Enter the IP address: ")

    if not args.live_id:
        args.live_id = user_input("Enter the Live ID: ")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.bind(("", 0))
    s.connect((args.ip_addr, XBOX_PORT))

    if isinstance(args.live_id, str):
        live_id = args.live_id.encode()
    else:
        live_id = args.live_id

    if not args.pingonly:
        power_payload = b'\x00' + chr(len(live_id)).encode() + live_id.upper() + b'\x00'
        power_header = b'\xdd\x02\x00' + chr(len(power_payload)).encode() + b'\x00\x00'
        power_packet = power_header + power_payload
        print("Sending power on packets to {0}...".format(args.ip_addr))
        send_power(s, power_packet)

        print("Xbox should turn on now, pinging to make sure...")
    ping_result = send_ping(s)

    if ping_result:
        print("Ping successful!")
    else:
        print("Failed to ping Xbox :(")
        result = ""
        if not args.forever and not args.pingonly:
            while result not in ("y", "n"):
                result = user_input("Do you wish to keep trying? (y/n): ").lower()
        if args.forever or result == "y":
            if not args.pingonly:
                print("Sending power packets and pinging until Xbox is on...")
            else:
                print("Sending pinging until Xbox is on...")
            while not ping_result:
                if not args.pingonly:
                    send_power(s, power_packet)
                ping_result = send_ping(s)
                print("Failed to ping Xbox :(")
            print("Ping successful!")

    s.close()


def send_power(s, data, times=5):
    for i in range(0, times):
        s.send(data)
        time.sleep(1)


def send_ping(s):
    s.send(bytearray.fromhex(XBOX_PING))
    return select.select([s], [], [], 5)[0]


def user_input(text):
    response = ""

    while response == "":
        if py3:
            response = input(text)
        else:
            response = raw_input(text)

    return response

if __name__ == "__main__":
    main()
