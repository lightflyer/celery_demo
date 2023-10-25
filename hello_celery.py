#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/8 15:46
# @Author  : streamer
# @File    : hello_celery.py
# @Project : celery_demo
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/6/8   CREATE
import random
import time

from typing import Dict, Any

import config

from celery import Celery
from celery.signals import task_prerun, task_postrun, task_success, task_failure, task_revoked, task_retry
from functools import wraps

class Square(object):
    def square(self, a):
        return a ** 2


class HelloWorld(Celery):
    calculator = None
    task_manager: Dict[Any, Any] = None

    def on_init(self):
        self.init_calc()
        self.register_square()

    def init_calc(self):
        self.task_manager = dict()
        self.calculator = Square()

    def register_div(self):
        def div(a, b):
            print(f'{self.main}:{a} / {b} = {a / b}')
            return a / b

        self.task(div)

    def register_square(self):
        # self.init_calc()

        def f(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper
        result = self.task(f(self.calculator.square), name='calculator.square')
        print(result, f'type:{type(result)}')
        self.task_manager[self.calculator.square] = result
        print(self.task_manager)
        print('register_square_finished')
        # result.delay(2)

    def yield_task(self, *a, **k):
        print(f'a:{a}, type:{type(a)}')
        print(f'k:{k}')

        def wrapper(func):
            @wraps(func)
            def crawl(*args, **kwargs):
                result = []
                for i in func(*args, **kwargs):
                    print(f'hello world ---- {i}')
                    result.append(i)
                return result
            new_args = (crawl, ) + a[1:]
            return self.task(*new_args, **k)
        if len(a) == 1 and callable(a[0]):
            return wrapper(a[0])
        else:
            return wrapper

    def worker_main(self, argv=None):
        self.register_div()
        print('register_div_finished')
        # self.register_square()

        print('now start celery')
        super().worker_main(argv)

    def start_calc(self, num=100):
        tasks = {}
        for i in range(num):
            for name, task in self.tasks.items():
                # print(self.main)
                if 'hello_celery' in name:
                    pass
                else:
                    continue
                a, b = random.randint(1, (i + 1) * 10), random.randint(1, i + 10)
                print(f'{name}{i}({a}, {b})')
                # result = task.delay(a, b)
                tasks[f'{name}{i}({a}, {b})'] = task.delay(a, b)
        return tasks


app = HelloWorld(
    'hello_celery',
    # broker='redis://localhost:6379/0',
    # result_backend='mongodb://localhost:27017/',
    # mongodb_backend_settings={
    #     'database': 'my_test',
    #     'taskmeta_collection': 'hello_celery',
    # },
    broker_connection_retry_on_startup=True,
    # task_routes={
    #     'hello_celery.add': {'queue': 'add'},
    #     'hello_celery.sub': {'queue': 'sub'},
    #     'hello_celery.mul': {'queue': 'mul'},
    #     'hello_celery.create_data': {'queue': 'new'},
    # },
    # include=['celery_demo.hello_celery,']
)


class MyTask(app.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print(f'{self.name} success: {retval}')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f'{self.name} failure: {exc}')


app.config_from_object(config)


class Calculator(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def run(self):
        raise NotImplementedError


class Addition(Calculator):
    def run(self):
        return self.a + self.b


class Subtraction(Calculator):
    def run(self):
        return self.a - self.b


@app.task
def add(a, b):
    return a + b


@app.task
def sub(a, b):
    return a - b


@app.task
def mul(a, b):
    return a * b


# @task_postrun.connect
# def process_calc(sender, task_id, task, args, kwargs, retval, **_):
#     if task.name == 'hello_celery.create_data':
#         for a, b in retval:
#             add.delay(a, b)
#             sub.delay(a, b)
#             mul.delay(a, b)
#         task.request.result = 'ok'


def process_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        result = 0
        for i, j in data:
            add.delay(i, j)
            sub.delay(i, j)
            mul.delay(i, j)
            result += i + j
        return result

    return wrapper


@app.task
@process_data
def create_data(i, j):
    for x in range(i):
        for y in range(j):
            yield x, y


@app.task
def depth_task(i, j):
    if i > 0 and j > 0:
        add.delay(i, j)
        sub.delay(i, j)
        mul.delay(i, j)
        depth_task.delay(i - 1, j - 1)
        return ['add', 'sub', 'mul', 'depth_task']
    return []


@app.task
def hello_world(word):
    print(f'hello world, {word}')
    child_hello.delay(word)


@app.task
def child_hello(word):
    print(f"fuck world, i'm pandas; {word}")


@app.yield_task(name='yield-change')
def yield_hello(num):
    for i in range(1, num + 1):
        yield f'yield hello {i}'


@app.yield_task
def yield_num(num):
    for i in range(1, num + 1):
        yield f'yield num {i}'


if __name__ == '__main__':
    app.worker_main(argv=['worker', '--loglevel=info', '--pool=threads', '--concurrency=200',
                          # '--queues=add,sub,mul,new'
                          ])
