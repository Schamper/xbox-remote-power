xbox-remote-power
======================

This is a little script that can turn your Xbox One on remotely. It works over both LAN and WAN, provided you have port 5050 forwarded to your Xbox One. Pretty much a first timer to python so beware of bad code.

## How to use

You need three things for this to work:
- Python 2 or 3 installed
- IP address of your Xbox One
- Live device ID of your Xbox One (not always needed)

To find the IP of your Xbox, go to Settings -> Network -> Advanced settings.  
To find your Live device ID, go to Settings -> System -> Console info.  
NOTE: It's probably a good idea to keep this information a secret!

If you want to use this over the internet, you'll also need port 5050 forwarded to your Xbox One.

Run the script as follows, replacing <ip address> with the IP of your Xbox and <live id> with your Live device ID.

```
python xbox-remote-power.py -a <ip address> -i <live id>
```

Alternatively, you can also run the script without any arguments and you'll be prompted for the IP and Live device ID.  
The script can also "ping" your Xbox for the Live ID but this doesn't always seem to work. To let it try and ping for your Live device ID, simply run the script without the `-i` argument or without any argument. If it fails, you will be prompted for your Live ID anyways.

```
python xbox-remote-power.py
```

There is also a "fire and forget" BAT script and shell script available. You will need to edit these files first and enter your IP and Live device ID before they will work.