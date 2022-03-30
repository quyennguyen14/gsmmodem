# -*- coding: utf-8 -*-
import hashlib
import requests
import traceback
import logging
from config import config_app
import mysql.connector

def md5_string(string):
    return hashlib.md5(string).hexdigest()

def sign_generate(BankTransferCode, secretKey, BankTransRefID, Amount):
    string = str(BankTransferCode) + '|' + str(secretKey)  + '|' + str(BankTransRefID) + '|' + str(Amount)
    return md5_string(string)

def postApi(url, BankTransferCode, secretKey, Amount, BankTransRefID):
    PARAMS = {
                "BankTransferCode":BankTransferCode,
                "Amount":Amount,
                "BankTransRefID":BankTransRefID,
                "Sign":sign_generate(BankTransferCode=BankTransferCode, secretKey=secretKey, BankTransRefID=BankTransRefID, Amount=Amount)
            }
    try:
        r = requests.post(url = url, data = PARAMS)

        return r.text
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())
        return {"ResponseCode":-99}

def splitMessage(textMessage):

    try:
        textMessage = textMessage.replace('.', '').replace(',','').replace('VND','').upper()
        textMessage = ''.join(textMessage.splitlines())
        textSub1 = textMessage[textMessage.index('(+) ') + 4:len(textMessage)]

        try:
            textSub2 = textMessage[textMessage.index('PAY ') + 4:len(textMessage)]
        except:
            return -1, 'Không phải bản tin cần xử lý'

        Amount = textSub1[:textSub1.index(' ')].strip()

        BankTransferCode = textSub2[:6].strip()

        if len(BankTransferCode) != 6:
            return -1, 'BankTransferCode khong hop le'

        return Amount, BankTransferCode
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())
        return -1, -1

def sp_insert_success_sms(time, textMessage, Amount, BankTransferCode):
    configInfo = config_app()
    configData = configInfo.config_mysql()
    host = configData["host"]
    user = configData["user"]
    password = configData["password"]
    database = configData["database"]

    logging.basicConfig(
       filename="logs/app.log",
       format="%(asctime)s - %(levelname)s - %(message)s",
       level=logging.INFO,
       encoding="UTF-8"
    )

    try:
        mydb = mysql.connector.connect(
                  host=host,
                  user=user,
                  password=password,
                  database=database,
                  auth_plugin='mysql_native_password'
                )

        cursor = mydb.cursor()


        args = [time, textMessage, Amount, BankTransferCode, 0, '']
        resultProc = cursor.callproc('SP_Log_bankTransferOffline_success_insert', args)

        p_ResponseStatus = resultProc[4]
        p_ResponseText = resultProc[5]

        return p_ResponseStatus, p_ResponseText

    except Exception as e:
        logging.error(format(e))
        logging.error(str(traceback.format_exc()))

def sp_insert_failed_sms(time, textMessage, Amount, BankTransferCode):
    configInfo = config_app()
    configData = configInfo.config_mysql()
    host = configData["host"]
    user = configData["user"]
    password = configData["password"]
    database = configData["database"]

    logging.basicConfig(
       filename="logs/app.log",
       format="%(asctime)s - %(levelname)s - %(message)s",
       level=logging.INFO,
       encoding="UTF-8"
    )

    try:
        mydb = mysql.connector.connect(
                  host=host,
                  user=user,
                  password=password,
                  database=database,
                  auth_plugin='mysql_native_password'
                )

        cursor = mydb.cursor()


        args = [time, textMessage, Amount, BankTransferCode, 0, '']
        resultProc = cursor.callproc('SP_Log_bankTransferOffline_failed_insert', args)

        p_ResponseStatus = resultProc[4]
        p_ResponseText = resultProc[5]

        return p_ResponseStatus, p_ResponseText

    except Exception as e:
        logging.error(format(e))
        logging.error(str(traceback.format_exc()))

def sp_get_sms_failed():
    configInfo = config_app()
    configData = configInfo.config_mysql()
    host = configData["host"]
    user = configData["user"]
    password = configData["password"]
    database = configData["database"]

    logging.basicConfig(
       filename="logs/app.log",
       format="%(asctime)s - %(levelname)s - %(message)s",
       level=logging.INFO,
       encoding="UTF-8"
    )

    try:
        mydb = mysql.connector.connect(
                  host=host,
                  user=user,
                  password=password,
                  database=database,
                  auth_plugin='mysql_native_password'
                )

        cursor = mydb.cursor()

        cursor.callproc('sp_get_sms_failed')

        for result in cursor.stored_results():
            return result.fetchall()

    except Exception as e:
        logging.error(format(e))
        logging.error(str(traceback.format_exc()))

def sp_update_status(LogId):
    configInfo = config_app()
    configData = configInfo.config_mysql()
    host = configData["host"]
    user = configData["user"]
    password = configData["password"]
    database = configData["database"]

    logging.basicConfig(
       filename="logs/app.log",
       format="%(asctime)s - %(levelname)s - %(message)s",
       level=logging.INFO,
       encoding="UTF-8"
    )

    try:
        mydb = mysql.connector.connect(
                  host=host,
                  user=user,
                  password=password,
                  database=database,
                  auth_plugin='mysql_native_password'
                )

        cursor = mydb.cursor()


        args = [LogId, 0, '']
        resultProc = cursor.callproc('sp_update_status', args)

        p_ResponseStatus = resultProc[1]
        p_ResponseText = resultProc[2]

        return p_ResponseStatus, p_ResponseText

    except Exception as e:
        logging.error(format(e))
        logging.error(str(traceback.format_exc()))

#  BankTransferCode = 'WJN9K3'
#  secretKey = 'T$123UhKV45ewr4)(!*6'
#  BankTransRefID = 'abc123'
#  Amount = '100000'
#  urlApi="https://vtcpay.vn/quantri/Transaction/BankTransferOffline_ConfirmBySIM"
#
#  response = postApi(url=urlApi, BankTransferCode=BankTransferCode, secretKey=secretKey, Amount=Amount, BankTransRefID=BankTransRefID)
#  print(response)
#  if __name__ == '__main__':
#      textMessage = "29/03 18:33 TK VND 031xx8869 (+) 200,000 (Thue/Phi: 0)Tu ND: -595440-MSB03101010508869PAY F3482GSD: 1.280.000)"
#      amount, code = splitMessage2(textMessage=textMessage)
#      print(amount)
#      print(code)
