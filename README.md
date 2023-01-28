# fc-exchange-rate-update

This is a simple Function Compute (FC) written in Python which fetches the updated data (in JSON format) from the [Exchange Rate API](https://www.exchangerate-api.com/) and upload it to an Aliyun OSS bucket. It is intended to be used in a [custom container](https://www.alibabacloud.com/help/en/function-compute/latest/create-a-function)-sourced function [triggered by a timer](https://www.alibabacloud.com/help/en/function-compute/latest/configure-a-time-trigger)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
