import logging

#Function to connect to vpn. It has to be installed and logged in to be used.
def refresh_vpn():
    import os
    import time

    logging.info("Refreshing VPN")
    os.popen("vyprvpn d")
    time.sleep(3)

    while True:
        r2 = os.popen("vyprvpn c")
        response = r2.readlines()
        if response[0] == 'Success! VyprVPN Connected\n':
            return True
        else:
            time.sleep(20)
