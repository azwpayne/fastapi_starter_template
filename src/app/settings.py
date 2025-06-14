#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File    : settings.py
# @Author  : Payne
# @Email   : paynewu0719@gmail.com
# @Github  : https://github.com/azwpayne 
# @Time    : 2025/6/13 23:05
# @Abstract:
import shutil
import sys
from contextvars import ContextVar
from datetime import datetime
from multiprocessing import cpu_count
from os.path import dirname, abspath, join
from random import randint

from environs import Env
from loguru import logger

env = Env()
env.read_env()

DATE_FORMAT = datetime.now().strftime("%Y%m%d_%H%M")  # "%Y%m%d_%H%M%S_%f"

ROOT_DIR = dirname(dirname(abspath(__file__)))
LOG_DIR = join(dirname(ROOT_DIR), env.str("LOG_DIR", f"logs/{DATE_FORMAT}/"))

DEV_MODE, TEST_MODE, PRE_MODE, PROD_MODE = "dev", "test", "pre", "prod"
APP_ENV = env.str("APP_ENV", DEV_MODE).lower()

APP_DEV = IS_DEV = APP_ENV == DEV_MODE
APP_TEST = IS_TEST = APP_ENV == TEST_MODE
APP_PRE = IS_PRE = APP_ENV == PRE_MODE
APP_PROD = IS_PROD = APP_ENV == PROD_MODE

ENABLE_LOG_FILE = env.bool("ENABLE_LOG_FILE", True)
ENABLE_LOG_RUNTIME_FILE = env.bool("ENABLE_LOG_RUNTIME_FILE", True)
ENABLE_LOG_ERROR_FILE = env.bool("ENABLE_LOG_ERROR_FILE", True)

LOG_LEVEL_MAP = {
    DEV_MODE: "DEBUG",
    TEST_MODE: "INFO",
    PRE_MODE: "WARNING",
    PROD_MODE: "ERROR",
}

LOG_LEVEL = LOG_LEVEL_MAP.get(APP_ENV)
LOG_ROTATION = env.str("LOG_ROTATION", "500MB")
LOG_RETENTION = env.str("LOG_RETENTION", "1 week")
LOG_ROTATION_COMPRESSION = env.str("LOG_ROTATION_COMPRESSION", "gz")

logger.remove()  # 移除默认配置

# 开发环境终端输出（美观格式）
logger.add(
    level="DEBUG",
    sink=sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{process}</cyan>:<cyan>{thread}</cyan> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "<level>{message}</level>",
    colorize=True,
    enqueue=True,
    backtrace=True,
    diagnose=True
)

if ENABLE_LOG_FILE:
    if ENABLE_LOG_RUNTIME_FILE:
        logger.add(
            env.str("LOG_RUNTIME_FILE", str(join(LOG_DIR, "runtime.log"))),
            level=LOG_LEVEL,
            rotation=LOG_ROTATION,
            retention=LOG_RETENTION,
            compression=LOG_ROTATION_COMPRESSION,
            enqueue=True,
            serialize=True,
            backtrace=True,
            diagnose=True
        )
    if ENABLE_LOG_ERROR_FILE:
        logger.add(
            env.str("LOG_RUNTIME_FILE", str(join(LOG_DIR, "error.log"))),
            level="ERROR",
            rotation=LOG_ROTATION,
            retention=LOG_RETENTION,
            compression=LOG_ROTATION_COMPRESSION,
            enqueue=True,
            serialize=True,
            backtrace=True,  # 启用异常堆栈
            diagnose=True  # 显示诊断信息
        )
else:
    shutil.rmtree("logs", ignore_errors=True)

# 配置请求ID上下文变量
request_id_ctx = ContextVar("request_id", default="")
SENSITIVE_KEYS = ["password", "token", "authorization"]  # 敏感字段过滤
WORKER_COUNT = env.int("WORKER_COUNT", randint(2, cpu_count() + 1))
