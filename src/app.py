###############################################################################
## FC to update the data from the Exchange-Rate-API. See README.md file.
## Copyright 2023 Rodolfo González González.
##
## The MIT license:
##
## Copyright 2023 Rodolfo Gonzalez <rodolfo.gonzalez@gmail.com>
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
## THE SOFTWARE.
##
## See LICENSE file for more details.

import oss2
import urllib3
import sys
import os

from rich.pretty import pprint

from exchange_rate_update import ExchangeRateUpdate

from config import Config

###############################################################################

try:
    # URLLib
    http = urllib3.PoolManager()

    """This should return at least a dictionary with this elements:
    ['EXCHANGE_RATE']['API']
    containing the URL of the Exchange Rate API
    """
    config = Config()

    # OSS
    auth = oss2.StsAuth(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
                        os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'],
                        os.environ['ALIBABA_CLOUD_SECURITY_TOKEN'])
    oss = oss2.Bucket(auth, config.config['OSS']['ENDPOINT'], config.config['OSS']['BUCKETS']['EXCHANGE_RATE'])

    file = 'exchangerate-api.json'
except Exception as ex:
    pprint(ex)
    sys.exit("Can not init script")

###############################################################################

# Called by FC using a time trigger (if using the free ER API, do it every 1
# or 2 hours)
if __name__ == '__main__':
    try:
        er = ExchangeRateUpdate(config, http, oss, file)
        ret = er.update()
        if ret == ExchangeRateUpdate.ERROR_OK:
            print("Exchange rate data updated.")
        elif ret == ExchangeRateUpdate.ERROR_CANT_GET_DATA:
            print("Can not get data from Exchange Rate service.")
        elif ret == ExchangeRateUpdate.ERROR_CANT_UPLOAD_FILE:
            print("Can not upload data file to OSS.")
        elif ret == ExchangeRateUpdate.ERROR_CANT_WRITE_FILE:
            print("Could not write temporary file.")

    except Exception as ex:
        pprint(ex)
# main