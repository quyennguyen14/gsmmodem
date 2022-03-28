from __future__ import print_function
from config import config_app
import logging

from gsmmodem.modem import GsmModem


def main():
    try:
        USSD = "*100*"

        configInfo = config_app()
        configData = configInfo.config_app()

        PORT = configData["port"]
        BAUDRATE = int(configData["baudrate"])
        TelcoCardCode = configData["TelcoCardCode"]

        USSD_STRING = USSD + TelcoCardCode + "#"
        PIN = None  # SIM card PIN (if any)

        print("Initializing modem...")
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
        modem = GsmModem(PORT, BAUDRATE)
        modem.connect(PIN)
        #
        modem.waitForNetworkCoverage(10)
        print("Sending USSD string: {0}".format(USSD_STRING))
        response = modem.sendUssd(USSD_STRING)  # response type: gsmmodem.modem.Ussd
        print("USSD reply received: {0}".format(response.message))
        if response.sessionActive:
            print("Closing USSD session.")
            # At this point, you could also reply to the USSD message by using response.reply()
            response.cancel()
        else:
            print("USSD session was ended by network.")
        modem.close()
    except:
        print("Close session...")
        modem.close()


if __name__ == "__main__":
    main()
