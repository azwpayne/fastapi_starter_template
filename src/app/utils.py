#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File    : utils.py
# @Author  : Payne
# @Email   : paynewu0719@gmail.com
# @Github  : https://github.com/azwpayne
# @Time    : 2025/6/13 23:07
# @Abstract:
import json
import os
import time
from contextlib import asynccontextmanager
from copy import deepcopy
from typing import Dict, Any, Optional
from uuid import uuid4

from fastapi import Request, Response, FastAPI
from loguru import logger
from pydantic import BaseModel

from src.app.settings import request_id_ctx, SENSITIVE_KEYS


class RequestLogSchema(BaseModel):
    request_id: str
    method: str
    path: str
    query_params: Dict[str, Any]
    client_ip: str
    user_agent: str
    request_body: Optional[Any]


class ResponseLogSchema(BaseModel):
    request_id: str
    status_code: int
    response_time: float  # 单位秒
    response_body: Optional[Any]


def filter_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    过滤敏感信息

    Args:
        data:

    Returns:

    """
    if not isinstance(data, dict):
        # 可根据需求改为 raise TypeError 或记录日志
        return data

    result = deepcopy(data)

    def _filter(d):
        for key in list(d.keys()):
            if key in SENSITIVE_KEYS:
                d[key] = '***REDACTED***'
            elif isinstance(d[key], dict):
                _filter(d[key])
            elif isinstance(d[key], list):
                for item in d[key]:
                    if isinstance(item, dict):
                        _filter(item)

    _filter(result)
    return result


async def log_request(request: Request) -> RequestLogSchema:
    """
    记录请求日志
    Args:
        request:

    Returns:

    """
    # 获取请求ID（用于串联请求）
    request_id = request.headers.get('X-Request-ID', str(uuid4().hex))
    request_id_ctx.set(request_id)

    # 读取并解析请求体
    request_body = None
    if request.method in ('POST', 'PUT', 'PATCH'):
        content_type = request.headers.get('content-type', '').lower()

        try:
            if any(ct in content_type for ct in ('application/json',)):
                request_body = await request.json()
                request_body = filter_sensitive_data(request_body)
            elif any(
                    ct in content_type
                    for ct in ('application/x-www-form-urlencoded', 'multipart/form-data')
            ):
                request_body = await request.form()
            else:
                content_length_str = request.headers.get('content-length', '0')
                try:
                    content_length = int(content_length_str)
                except ValueError:
                    content_length = 0

                if content_length < 1024:
                    request_body = (await request.body()).decode(errors='ignore')
        except Exception as e:
            # 记录解析失败原因，不影响主流程
            request_body = {'_error': f'Failed to parse request body: {str(e)}'}

    return RequestLogSchema(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        query_params=dict(request.query_params),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get('user-agent'),
        request_body=request_body,
    )


async def log_response(response: Response, response_time: float) -> ResponseLogSchema:
    """
    记录响应日志
    Args:
        response:
        response_time:

    Returns:
    """
    request_id = request_id_ctx.get()
    response_body = None

    # 解析响应内容
    if hasattr(response, 'body'):
        content_type = response.headers.get('content-type', '').lower()

        try:
            body = response.body
            if 'application/json' in content_type:
                if isinstance(body, bytes):
                    body = body.decode()
                if isinstance(body, str):
                    response_body = json.loads(body)
                # 若 body 已是 dict/list 等结构，直接使用
                elif isinstance(body, (dict, list)):
                    response_body = body
                else:
                    # 不支持的类型不记录 body
                    pass

                response_body = filter_sensitive_data(response_body)

        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            # 明确捕获并记录解码/解析错误
            logger.warning(f'Failed to decode response body: {e}')

    return ResponseLogSchema(
        request_id=request_id,
        status_code=response.status_code,
        response_time=response_time,
        response_body=response_body,
    )


@asynccontextmanager
async def lifespan(a: FastAPI):
    """应用生命周期管理"""
    # configure_logger()
    logger.info(f'🚀 Worker {os.getpid()} started')
    try:
        yield
    finally:
        logger.info(f'🛑 Worker {os.getpid()} shutting down')
        # Loguru 会自动处理关闭


app = FastAPI(debug=False, lifespan=lifespan)


@app.middleware('http')
async def logging_middleware(request: Request, call_next):
    """
    全局日志中间件
    Args:
        request:
        call_next:

    Returns:
    """
    start_time = time.perf_counter()

    # 请求日志
    request_log = await log_request(request)
    logger.info(
        f'Request received client_ip:{request.client.host} user-agent:{request.headers.get("user-agent")}',
        extra={'type': 'request', 'data': request_log.model_dump()},
    )

    response = None  # 提前定义 response
    try:
        response = await call_next(request)
    except Exception as exc:
        # 异常日志（带堆栈跟踪）
        logger.exception('Request processing failed', extra={'request_id': request_log.request_id})
        raise exc from None
    finally:
        # 响应日志
        response_time = time.perf_counter() - start_time
        response_log = await log_response(response, response_time)
        logger.info('Response sent', extra={'type': 'response', 'data': response_log.model_dump()})

    response.headers['X-Request-ID'] = request_id_ctx.get()
    return response
