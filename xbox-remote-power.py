import sys, getopt, socket, select, time, codecs, binascii

xbox_port = 5050
xbox_ping = "dd00000a000000000000000400000002"
xbox_power = "dd02001300000010"

help_text = "xbox-remote-power.py -a <ip address> -i <live id>"

py3 = sys.version_info[0] > 2

def main(argv):
    ip_addr = ""
    live_id = ""
    
    try:
        opts, args = getopt.getopt(argv,"ha:i:",["address=","id="])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_text)
            sys.exit()
        elif opt in ("-a", "--address"):
            ip_addr = arg
        elif opt in ("-i", "--id"):
            live_id = arg

    if ip_addr == "":
        ip_addr = user_input("Enter the IP address: ")

    ping = False
    if live_id == "":
        print("No Live ID given, do you want to attempt to ping the Xbox for it?")
        result = ""
        while result not in ("y", "n"):
            result = user_input("(y/n): ")
        if result == "y":
            ping = True
        if result == "n":
            live_id = user_input("Enter the Live ID: ")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.bind(("", 0))
    s.connect((ip_addr, xbox_port))

    if ping:
        print("Attempting to ping Xbox for Live ID...")
        if py3:
            s.send(bytes.fromhex(xbox_ping))
        else:
            s.send(xbox_ping.decode("hex"))

        ready = select.select([s], [], [], 5)
        if ready[0]:
            data = s.recv(1024)
            live_id = data[199:215]
        else:
            print("Failed to ping Xbox, please enter Live ID manually")
            live_id = user_input("Enter the Live ID: ")

    if isinstance(live_id, str):
        live_id = live_id.encode()

    if py3:
        power_packet = bytes.fromhex(xbox_power)
        power_packet = power_packet + live_id + b'\x00'
    else:
        power_packet = xbox_power + live_id.encode("hex") + "00"
        power_packet = power_packet.decode("hex")

    print("Sending power on packets to " + ip_addr)
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
    main(sys.argv[1:])
