#!/usr/bin/env python
from __future__ import print_function
import logging
from gsmmodem.modem import GsmModem
from config import config_app


def handleSms(sms):

    text_message = sms.text
    logMess = "== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n".format(
            sms.number, sms.time, text_message.encode("utf-8")
        )
    logging.basicConfig(filename="appLog.log", format="%(levelname)s: %(message)s", level=logging.INFO)

    print(logMess)
    print("From: {0}".format(sms.number))
    print("Time: {0}".format(sms.time))
    print("Text_message: {0}".format(text_message.encode("utf-8")))


def main():
    configInfo = config_app()
    configData = configInfo.config_app()

    PORT = configData["port"]
    BAUDRATE = int(configData["baudrate"])
    PIN = None

    print("Initializing modem...")
    # Uncomment the following line to see what the modem is doing:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = False
    modem.connect(PIN)
    print("Waiting for SMS message...")

    try:
        modem.rxThread.join(
            2**31
        )  # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
    finally:
        modem.close()


if __name__ == "__main__":
    main()
