#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/26 18:30
# @Author  : streamer
# @File    : connect_redis.py
# @Project : celery_demo
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/6/26   CREATE

import redis

# 创建 Redis 连接
redis_host = 'localhost'
redis_port = 6379

try:
    r = redis.Redis(host=redis_host, port=redis_port, db=0)

    # 在 Redis 中设置键值对
    r.set('mykey', 'Hello, Redis!')

    # 从 Redis 中获取值
    value = r.get('mykey')
    print(value.decode('utf-8'))  # 将二进制数据转换为字符串

    # 可以执行其他 Redis 操作...

except redis.RedisError as e:
    print(f"连接 Redis 出错: {str(e)}")
