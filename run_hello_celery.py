#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/8 15:55
# @Author  : streamer
# @File    : run_hello_celery.py
# @Project : celery_demo
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/6/8   CREATE
import random
import time
from pprint import pprint

from celery.result import AsyncResult

from hello_celery import add, sub, mul, create_data, depth_task, yield_num
from hello_celery import app, yield_hello


def run(n):
    start_time = time.time()
    add_results, sub_results, mul_result = [], [], []
    for i in range(100):
        a, b = random.randint(0, i * n), random.randint(0, i + n)
        add_results.append(add.delay(a, b))
        sub_results.append(sub.delay(a, b))
        mul_result.append(mul.delay(a, b))

    for idx, result in enumerate(add_results):
        # print(f'add({idx})={result.get(timeout=60)}')
        # print(f'sub({idx})={sub_results[idx].get(timeout=60)}')
        print(f'mul({idx})={mul_result[idx].get(timeout=60)}')
    print('cost time:', time.time() - start_time)


def start_run():
    app.start_calc()


def add_new_data(num):
    start_time = time.time()
    add_results, sub_results, mul_result, new_result = [], [], [], []
    for i in range(num):
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        add_results.append(add.delay(x, y))
        sub_results.append(sub.delay(x, y))
        mul_result.append(mul.delay(x, y))
        new_result.append(create_data.delay(x, y))

    for idx, result in enumerate(add_results):
        print(f'add({idx})={result.get(timeout=60)}')
        print(f'sub({idx})={sub_results[idx].get(timeout=60)}')
        print(f'mul({idx})={mul_result[idx].get(timeout=60)}')
        print(f'new({idx})={new_result[idx].get(timeout=3600)}')
    print('cost time:', time.time() - start_time)


def run_start_calc(num):
    start_time = time.time()
    tasks = app.start_calc(num)
    for name, result in tasks.items():
        print(f'{name}={result.get(timeout=3600)}')
    print('cost time:', time.time() - start_time)


def run_third_depth(i, j):
    start_time = time.time()
    result = depth_task.delay(i, j)
    print(f'depth_task({i, j}) id = {result.id}')
    # print(f'depth_task({i, j})={result.get(timeout=3600)}')
    print('cost time:', time.time() - start_time)


def get_related_tasks(task_id):
    """根据任务 ID 获取由这个任务衍生的所有任务"""
    async_result = AsyncResult(task_id)

    # print(async_result.result)
    # 查找所有衍生的子任务 ID
    children_ids = [child.id for child in async_result.children]

    # # 递归获取所有衍生的子任务及其子任务
    related_ids = set(children_ids)
    for child_id in children_ids:
        related_ids |= set(get_related_tasks(child_id))

    related_ids = set(related_ids)
    pprint(related_ids)

    return related_ids


def get_task_result(task_id):
    """根据任务 ID 获取任务的结果"""
    result = {
        'child': 0,
        'success': 0,
        'failure': 0,
        'pending': 0,
        'retry': 0,
        'started': 0,
        'unknown': 0,
        'result': []
    }
    async_result = AsyncResult(task_id)

    child = [child.id for child in async_result.children] or []
    while len(child) > 0:
        for c_id in child:
            result['child'] += 1
            c = AsyncResult(c_id)
            if c.state in ['SUCCESS', 'FAILURE']:
                if c.state == 'SUCCESS':
                    result['result'].append(c.result)
                result[c.state.lower()] += 1
            else:
                result[c.state.lower()] += 1
            child.extend([item.id for item in c.children] or [])
            child.remove(c_id)
    return {
        'task_id': task_id,
        'task_state': async_result.state,
        'result_info': result
    }


def run_yield_hello(num):
    results = [yield_hello.delay(i) for i in range(1, num + 1)]
    for result in results:
        print(result.get(timeout=60))


def run_yield_num(num):
    results = [yield_num.delay(i) for i in range(1, num + 1)]
    for result in results:
        print(result.get(timeout=60))


def run_task_dynamic():
    task = app.task_manager[app.calculator.square]
    results = [task.delay(i+1) for i in range(5)]
    for result in results:
        print(result.get(timeout=60))


if __name__ == '__main__':
    # run(5)
    # add_new_data(100)
    # run_start_calc(50)
    # run_third_depth(20, 20)
    # t_id = '92d3a6aa-8d8f-4133-8259-2bb50466b0c8'
    # r = get_task_result(t_id)
    # pprint(r)
    # print(len(get_related_tasks(t_id)))

    # run_yield_hello(10)
    # run_yield_num(10)
    run_task_dynamic()
