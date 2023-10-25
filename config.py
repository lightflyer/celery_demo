#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/9 16:22
# @Author  : streamer
# @File    : config.py
# @Project : celery_demo
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/7/9   CREATE
broker_url='redis://localhost:6379/0'
result_backend='mongodb://localhost:27017/'
mongodb_backend_settings={
    'database': 'my_test',
    'taskmeta_collection': 'hello_celery',
}