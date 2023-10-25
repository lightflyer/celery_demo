#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/11 17:38
# @Author  : streamer
# @File    : run_new_celery.py
# @Project : celery_demo
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/10/11   CREATE
from hello_celery import hello_world

if __name__ == '__main__':
    result = hello_world.apply_async(args=['value1', ], priority=5)
    print(result.get(timeout=60))