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

from config import Config

###############################################################################

try:
    # URLLib
    http = urllib3.PoolManager()

    # Config
    config = Config()

    # OSS
    auth = oss2.Auth(config.config['AUTH']['ACCESSKEY']['ID'], config.config['AUTH']['ACCESSKEY']['SECRET'])
    oss = oss2.Bucket(auth, config.config['OSS']['ENDPOINT'], config.config['OSS']['BUCKETS']['EXCHANGE_RATE'])

    file = 'exchangerate-api.json'

except Exception as ex:
    print(ex)
    sys.exit("Can not init script")

###############################################################################

## Get the data from Exchange Rate
def getRates():
    try:
        result = http.request("GET", config.config['EXCHANGE_RATE']['API'])

        return result.data.decode("utf-8")

    except Exception as ex:
        print(ex)
        return False
# getRates

###############################################################################

# Write data from Exchange Rate into a local file
def writeTemp(file, json):
    try:
        file = open(file, mode="w", encoding="utf-8")
        file.write(json)
        file.close()

        return True

    except Exception as ex:
        print(ex)
        return False
# writeTemp

###############################################################################

# Upload the local file to the OSS bucket.
def uploadRates(file):
    try:
        object = os.path.basename(file)
        oss.put_object_from_file(object, file)

    except Exception as ex:
        print(ex)
        return False

    return True
# uploadRates

###############################################################################

# Called by FC using a time trigger (if using the free ER API, do it every 1
# or 2 hours)
if __name__ == '__main__':
    try:
        jsonData = getRates()
        if jsonData != False:
            res = writeTemp('/tmp/' + file, jsonData)
            if res != False:
                res = uploadRates('/tmp/' + file)
                if res != False:
                    print("OK")
                else:
                    print("Could not upload the file to the bucket.")
            else:
                print("Could not write temporary file.")
        else:
            print("Could not get data from the exchange-rate-api service.")

    except Exception as ex:
        print(ex)