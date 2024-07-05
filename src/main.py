#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File    : main.py
# @Author  : PayneWu
# @Email   : paynewu0719@gmail.com
# @Github  : https://github.com/azwpayne 
# @Time    : 2024/7/5 上午11:13

import uvicorn
from fastapi import FastAPI

from src.fastapi_starter_template.app.api import router as api_router


def get_application() -> FastAPI:
    application = FastAPI(title="fastapi starter template")
    application.include_router(api_router)
    return application


app = get_application()

if __name__ == '__main__':
    uvicorn.run("src.main:app", workers=17)
