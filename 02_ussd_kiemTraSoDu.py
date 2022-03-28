from __future__ import print_function
from config import config_app
import logging
from gsmmodem.modem import GsmModem


def main():
    try:

        USSD_STRING = "*101#"

        configInfo = config_app()
        configData = configInfo.config_app()

        PORT = configData["port"]
        BAUDRATE = int(configData["baudrate"])
        PIN = None  # SIM card PIN (if any)

        print("Initializing modem...")
        modem = GsmModem(PORT, BAUDRATE)
        modem.connect(PIN)
        #
        modem.waitForNetworkCoverage(10)
        print("Sending USSD string: {0}".format(USSD_STRING))

        response = modem.sendUssd(USSD_STRING)  # response type: gsmmodem.modem.Ussd

        print("USSD reply received: {0}".format(response.message))
        logging.basicConfig(filename='logs/app.log', format="%(asctime)s: %(levelname)s: %(message)s", level=logging.INFO)
        logging.info("02_ussd_kiemTraSoDu.py | USSD reply received: {0}".format(response.message))

        if response.sessionActive:
            logging.info("Closing USSD session.")
            # At this point, you could also reply to the USSD message by using response.reply()
            response.cancel()
        else:
            logging.error("USSD session was ended by network.")
        modem.close()
    except:
        logging.error("Close session...")
        modem.close()


if __name__ == "__main__":
    main()
