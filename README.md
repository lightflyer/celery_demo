#演示完全不规则的文件夹目录，使用celery。

## 介绍两种运行celery消费的方式
#### 1.使用python xxx.py的方式启动消费
#### 2.使用celery 命令的方式启动消费

项目目录结构是：
```

文件夹 PATH 列表
卷序列号为 927B-F991
F:.
│  .gitignore
│  nb_log_config.py
│  README.md
│  
│          
├─aaaa
│  └─b
│      └─c
│          │  celery_app_inatcance.py
│          │  
│          └─__pycache__
│                  celery_app_inatcance.cpython-36.pyc
│                  
├─dddd
│  ├─e
│  │  │  taske.py
│  │  │  
│  │  └─__pycache__
│  │          taske.cpython-36.pyc
│  │          
│  └─f
│      │  taskf.py
│      │  
│      └─__pycache__
│              taskf.cpython-36.pyc
│              
├─gggg
│      publish.py
│      

        
```

## 主代码
```python
# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2020/1/16 0016 9:40

"""
主要用用来测试深层文件夹，celery完全不按照特定目录结构写代码。
"""
import nb_log
import celery
from celery import platforms

platforms.C_FORCE_ROOT = True

class Config1:
    broker_url = f'redis://'  # 使用redis
    include = ['dddd.e.taske','dddd.f.taskf']

    task_routes = {
        '求和': {"queue": "queue_add", },
        # 'd.e.taske.add': {"queue": "queue_add4", },
        'sub啊': {"queue": 'queue_sub'},
    }

celery_app = celery.Celery()
celery_app.config_from_object(Config1)
print(type(celery_app))


if __name__ == '__main__':
    # celery_demo 项目在我的磁盘是 F:\coding2\celery_demo。

    # 第一种运行方式，直接运行此py脚本。如果在pycahrm中可以直接运行，如果控制台运行py脚本先设置PYTHONATH=F:\coding2\celery_demo，再python celery_app_inatcance.py 运行。
    celery_app.worker_main(
        argv=['worker','--pool=gevent', '--concurrency=20', '-n', 'worker1@%h', '--loglevel=debug',
              '--queues=queue_add,queue_sub', '--detach', ])

    """
    第二种运行方式，使用官方介绍的流行的celery命令行运行
    
    F: & cd F:\coding2\celery_demo 
    
    celery   worker --app=aaaa.b.c.celery_app_inatcance:celery_app --pool=gevent --concurrency=5  --queues=queue_add,queue_sub
    """

```