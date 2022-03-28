#!/usr/bin/env python

from __future__ import print_function
from gsmmodem.modem import GsmModem, Sms
from config import config_app
import logging
from datetime import datetime
import traceback
import Utils

def main():

    try:
        configInfo = config_app()
        configData = configInfo.config_app()

        PORT = configData["port"]
        BAUDRATE = int(configData["baudrate"])
        PIN = None

        # Uncomment the following line to see what the modem is doing:
        logging.basicConfig(
           filename="logs/app.log",
           format="%(asctime)s - %(levelname)s - %(message)s",
           level=logging.INFO,
           encoding="UTF-8"
        )

        logging.info('Initializing modem...')
        modem = GsmModem(PORT, BAUDRATE)
        modem.smsTextMode = False
        modem.connect(PIN)
        smss = modem.listStoredSms(status=Sms.STATUS_RECEIVED_READ, delete=True);

        logging.info("=============== Start Process ================")
        logging.info("05_delete_read_sms | {} read messages found".format(str(len(smss))))

    except Exception as e:
        logging.error("=============== Exception ===============")
        logging.error("05_delete_read_sms | {}".format(e))
        logging.error(str(traceback.format_exc(e)))
        modem.close()

if __name__ == "__main__":
    main()
