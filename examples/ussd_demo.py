from __future__ import print_function

import logging

PORT = '/dev/ttyUSB0'
BAUDRATE = 115200
USSD_STRING = '*101#'
PIN = None # SIM card PIN (if any)

from gsmmodem.modem import GsmModem

def main():
    print('Initializing modem...')
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE)
    modem.connect()
    # #
    # modem.waitForNetworkCoverage(10)
    # print('Sending USSD string: {0}'.format(USSD_STRING))
    # response = modem.sendUssd(USSD_STRING) # response type: gsmmodem.modem.Ussd
    # print('USSD reply received: {0}'.format(response.message))
    # if response.sessionActive:
    #     print('Closing USSD session.')
    #     # At this point, you could also reply to the USSD message by using response.reply()
    #     response.cancel()
    # else:
    #     print('USSD session was ended by network.')
    modem.close()

if __name__ == '__main__':
    main()
