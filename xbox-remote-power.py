import sys, socket, select, time
from optparse import OptionParser

XBOX_PORT = 5050
XBOX_PING = "dd00000a000000000000000400000002"
XBOX_POWER = "dd02001300000010"

help_text = "xbox-remote-power.py -a <ip address> -i <live id>"

py3 = sys.version_info[0] > 2

def main():
    parser = OptionParser()
    parser.add_option('-a', '--address', dest='ip_addr', help="IP Address of Xbox One", default='')
    parser.add_option('-i', '--id', dest='live_id', help="Live ID of Xbox One", default='')
    (opts, args) = parser.parse_args()
        
    if not opts.ip_addr:
        opts.ip_addr = user_input("Enter the IP address: ")

    ping = False
    if not opts.live_id:
        print("No Live ID given, do you want to attempt to ping the Xbox for it?")
        result = ""
        while result not in ("y", "n"):
            result = user_input("(y/n): ").lower()
        if result == "y":
            ping = True
        elif result == "n":
            opts.live_id = user_input("Enter the Live ID: ")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.bind(("", 0))
    s.connect((opts.ip_addr, XBOX_PORT))

    if ping:
        print("Attempting to ping Xbox for Live ID...")
        if py3:
            s.send(bytes.fromhex(XBOX_PING))
        else:
            s.send(XBOX_PING.decode("hex"))

        ready = select.select([s], [], [], 5)
        if ready[0]:
            data = s.recv(1024)
            opts.live_id = data[199:215]
        else:
            print("Failed to ping Xbox, please enter Live ID manually")
            opts.live_id = user_input("Enter the Live ID: ")

    if isinstance(opts.live_id, str):
        live_id = opts.live_id.encode()

    if py3:
        power_packet = bytes.fromhex(XBOX_POWER)
        power_packet = power_packet + opts.live_id + b'\x00'
    else:
        power_packet = XBOX_POWER + opts.live_id.encode("hex") + "00"
        power_packet = power_packet.decode("hex")

    print("Sending power on packets to " + opts.ip_addr)
    for i in range(0, 5):
        s.send(power_packet)
        time.sleep(1)
    print("Xbox should turn on now")

    s.close()

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
