#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/26 18:32
# @Author  : streamer
# @File    : run_flower.py
# @Project : celery_demo
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/6/26   CREATE
# from flower import start
#
# # Celery Broker URL
# broker_url = 'redis://localhost:6379/0'
#
# # Celery App Name
# app_name = 'my_celery_app'
#
# # Flower Configuration
# flower_options = {
#     'broker': broker_url,
#     'port': 5555  # Set the port number to listen on
# }
#
# # Start Celery Flower
from hello_celery import app
if __name__ == '__main__':
    app.start(argv=['--broker=redis://localhost:6379/0', 'flower', '--port=5555'])
