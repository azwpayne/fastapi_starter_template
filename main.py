#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File    : main.py
# @Author  : PayneWu
# @Email   : paynewu0719@gmail.com
# @Github  : https://github.com/azwpayne
# @Time    : 2024/7/5 上午11:13


from loguru import logger

from src.app.collectors import router as api_router
from src.app.settings import WORKER_COUNT
from src.app.utils import app

app.include_router(api_router)


@app.get('/')
async def root():
    logger.info('Hello World')
    return {'message': 'Hello World'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
        reload=False,
        workers=WORKER_COUNT,
        # log_config=None,  # 禁用Uvicorn默认日志，仅用Loguru
        # access_log=False,  # 禁用访问日志（使用自定义日志）
    )
