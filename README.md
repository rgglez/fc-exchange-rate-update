# fc-exchange-rate-update

This is a simple Aliyun Function Compute (FC) written in Python which fetches the data in JSON format from the [Exchange Rate API](https://www.exchangerate-api.com/) (go there to get a free key) and uploads it to an Aliyun OSS bucket. It is intended to be used in a [custom container](https://www.alibabacloud.com/help/en/function-compute/latest/create-a-function)-sourced function [triggered by a timer](https://www.alibabacloud.com/help/en/function-compute/latest/configure-a-time-trigger), but you can adapt it depeding on your needs.

## Notes

* The *config.py* file is not provided, as you may already have your own configuration file/system (perhaps even using the enviroment variables of the FC). Just replace the config.config dictionary members with your own cofiguration parameters.
* A sample *Dockerfile* in provided, which you might adjust to your use case.
* A sample *requirements.txt* file is provided, which you might adjust to your use case.
* The free API has certain quota, so setup the "cronjob" to be run every hour.
* Aliyun refers to Alibaba Cloud Services, but this code can be easily adapted to run in AWS Lambda, for instance.
* I am **not** affiliated in any way to Exchange-Rate-API. I found their API handy for some of my projects. You should check if their service suits your use case, both technically and legally.
* Please **read** the LICENSE file.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

Copyright 2023 Rodolfo González González.
