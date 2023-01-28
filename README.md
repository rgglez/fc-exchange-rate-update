# fc-exchange-rate-update

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a simple Function Compute (FC) written in Python which fetches the data in JSON format from the [Exchange Rate API](https://www.exchangerate-api.com/) and uploads it to an Aliyun OSS bucket. It is intended to be used in a [custom container](https://www.alibabacloud.com/help/en/function-compute/latest/create-a-function)-sourced function [triggered by a timer](https://www.alibabacloud.com/help/en/function-compute/latest/configure-a-time-trigger), but you can adapt it depeding on your needs.

## Notes

* The config.py file is not provided, as you may already have your own configuration file/system (perhaps even using the enviroment variables of the FC). Just replace the config.config dictionary members with your own cofiguration parameters.
