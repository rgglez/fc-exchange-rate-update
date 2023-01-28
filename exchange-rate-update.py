###############################################################################
## FC to update the data from the Exchange-Rate-API. See README.md file.
## Copyright (c) 2023 Rodolfo González González.
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