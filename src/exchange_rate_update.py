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

import os

class ExchangeRateUpdate:
    ###############################################################################

    ERROR_OK = 0
    ERROR_CANT_UPLOAD_FILE = 1
    ERROR_CANT_WRITE_FILE = 2
    ERROR_CANT_GET_DATA = 3

    ###############################################################################

    config = None
    http = None
    oss = None
    file = None

    ###############################################################################

    def __init__(self, config, http, oss, file) -> None:
        ExchangeRateUpdate.config = config
        ExchangeRateUpdate.http = http
        ExchangeRateUpdate.oss = oss
        ExchangeRateUpdate.file = file
    # __init__

    ###############################################################################

    ## Get the data from Exchange Rate
    def getRates(self):
        try:
            result = ExchangeRateUpdate.http.request("GET", 
                        ExchangeRateUpdate.config.config['EXCHANGE_RATE']['API'])

            return result.data.decode("utf-8")

        except Exception as ex:
            print(ex)
            return False
    # getRates

    ###############################################################################

    # Write data from Exchange Rate into a local file
    def writeTemp(self, json):
        try:
            file = open(ExchangeRateUpdate.file, mode="w", encoding="utf-8")
            file.write(json)
            file.close()

            return True

        except Exception as ex:
            print(ex)
            return False
    # writeTemp

    ###############################################################################

    # Upload the local file to the OSS bucket.
    def uploadRates(self):
        try:
            object = os.path.basename(ExchangeRateUpdate.file)
            ExchangeRateUpdate.oss.put_object_from_file(object, ExchangeRateUpdate.file)

        except Exception as ex:
            print(ex)
            return False

        return True
    # uploadRates

    ###############################################################################

    def update(self):
        jsonData = self.getRates()
        if jsonData != False:
            res = self.writeTemp('/tmp/' + ExchangeRateUpdate.file, jsonData)
            if res != False:
                res = self.uploadRates('/tmp/' + ExchangeRateUpdate.file)
                if res != False:
                    return ExchangeRateUpdate.ERROR_OK
                else:
                    return ExchangeRateUpdate.ERROR_CANT_UPLOAD_FILE
            else:
                return ExchangeRateUpdate.ERROR_CANT_WRITE_FILE
        else:
            return ExchangeRateUpdate.ERROR_CANT_GET_DATA
    # update
# ExchangeRateUpdate