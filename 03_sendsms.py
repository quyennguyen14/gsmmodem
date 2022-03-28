#!/usr/bin/env pythonrun python 2.7 on ubuntu 20.4
from __future__ import print_function
import sys, logging
from config import config_app
from gsmmodem.modem import GsmModem, SentSms
from datetime import datetime
from gsmmodem.exceptions import TimeoutException, PinRequiredError, IncorrectPinError

def main():
    now = datetime.now()

    configInfo = config_app()
    configData = configInfo.config_app()

    PORT = configData["port"]
    BAUDRATE = int(configData["baudrate"])
    SentTo = configData["sentSmsTo"]
    PIN = None  # SIM card PIN (if any)
    MESS_CONTENT = "Send mess: " + now.strftime("%d/%m/%Y %H:%M:%S")

    modem = GsmModem(PORT, BAUDRATE)
    modem.connect(PIN)
    modem.waitForNetworkCoverage(5)

    modem.sendSms(SentTo, MESS_CONTENT, waitForDeliveryReport=False)

    # Because the bug of modem, must reset modem after send a sms
    modem.write('AT+CFUN=1')
    modem.close()

    logging.basicConfig(filename='logs/app.log',format="%(asctime)s: %(levelname)s: %(message)s", level=logging.INFO)
    logging.info("Message Sent to {0}".format(SentTo))


    #  try:
    #      sms = modem.sendSms(SentTo, MESS_CONTENT, waitForDeliveryReport=True)
    #      logging.basicConfig(filename='logs/app.log',format="%(asctime)s: %(levelname)s: %(message)s", level=logging.INFO)
    #  except TimeoutException:
    #      logging.error('Failed to send message: the send operation timed out')
    #      modem.close()
    #      sys.exit(1)
    #  else:
    #      modem.close()
    #      if sms.report:
    #          logging.info('Message sent{0}'.format(' and delivered OK.' if sms.status == SentSms.DELIVERED else ', but delivery failed.'))
    #      else:
    #          logging.info('Message sent.')

if __name__ == "__main__":
    main()
