#!/usr/bin/env python

from __future__ import print_function
from gsmmodem.modem import GsmModem, Sms
from config import config_app
import logging
from datetime import datetime
import traceback
import Utils

def processSms(sms):
    configInfo = config_app()
    configData = configInfo.config_api()
    urlApi = configData["urlApi"]
    secretKey = configData["secretKey"]

    try:
        text_message = sms.text
        logMess = "Message Info: (smsTime: {}, smsNumber: {}, smsText: {})".format(str(sms.time)[0:19], sms.number, text_message.encode("utf-8)"))

        logging.info(logMess)

        Amount = -1

        if sms.number == 'MSB':
            Amount, BankTransferCode = Utils.splitMessage(text_message)
        else:
            logging.info("Message don't need process!")
            return

        if Amount != -1:
            response_text = Utils.postApi(url=urlApi,
                    BankTransferCode=BankTransferCode,
                    secretKey=secretKey,
                    Amount=Amount,
                    BankTransRefID='')

            logCallApi = response_text
            logging.info(logCallApi)
        else:
            logging.info("MSB, don't need process")

    except Exception as e:
        logging.error("=============== Exception ================")
        logging.error("04_loadUnreadSMS | {}".format(e))
        logging.error(str(traceback.format_exc()))

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
        #  smss = modem.listStoredSms(status=Sms.STATUS_ALL, delete=False)
        smss = modem.listStoredSms(status=Sms.STATUS_RECEIVED_UNREAD, delete=False)
        # smss = modem.listStoredSms(status=Sms.STATUS_RECEIVED_READ, delete=True)

        logging.info("=============== Start Process ================")
        logging.info("04_loadUnreadSMS.py | {} new messages found".format(str(len(smss))))

        if len(smss) > 0:
            for i in range(len(smss)):
                sms = smss[i]
                processSms(sms)
        else:
            logging.info("Nothing to do !")
        logging.info("=============== End Process ================")
        modem.close()

    except Exception as e:
        logging.error("=============== Exception ===============")
        logging.error("04_loadUnreadSMS | {}".format(e))
        logging.error(str(traceback.format_exc(e)))
        modem.close()

if __name__ == "__main__":
    main()
