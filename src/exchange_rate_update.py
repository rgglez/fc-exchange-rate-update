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

from rich.pretty import pprint

###############################################################################

class ExchangeRateUpdate:
    # Constants

    ERROR_OK = 0
    ERROR_CANT_UPLOAD_FILE = 1
    ERROR_CANT_WRITE_FILE = 2
    ERROR_CANT_GET_DATA = 3

    # Class variables

    config = None
    http = None
    oss = None
    file = None

    ###############################################################################

    def __init__(self, config=None, http=None, oss=None, file=None) -> None:
        ExchangeRateUpdate.config = config
        ExchangeRateUpdate.http = http
        ExchangeRateUpdate.oss = oss
        ExchangeRateUpdate.file = file
    # __init__

    ###############################################################################

    def getRates(self):
        """Gets the data from Exchange Rate.
        """
        try:
            result = self.http.request("GET",
                self.config.config['EXCHANGE_RATE']['API'])
            pprint(result)

            return result.data.decode("utf-8")

        except Exception as ex:
            pprint(ex)
            return False
    # getRates

    ###############################################################################

    def writeTemp(self, file, json):
        """Writes data from Exchange Rate into a local file.
        """
        try:
            file = open(file, mode="w", encoding="utf-8")
            file.write(json)
            file.close()

            return True

        except Exception as ex:
            pprint(ex)
            return False
    # writeTemp

    ###############################################################################

    def uploadRates(self, file):
        """Uploads the Exchange Rate data file into OSS.
        """
        try:
            object = os.path.basename(file)
            self.oss.put_object_from_file(object, file)

        except Exception as ex:
            pprint(ex)
            return False

        return True
    # uploadRates

    ###############################################################################

    def update(self):
        """Updates the Exchange Rate data.
        """
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

###############################################################################

if __name__ == "__main__":
    import doctest

    doctest.testmod()
# main
