#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File    : device_gen.py
# @Author  : Payne
# @Email   : paynewu0719@gmail.com
# @Github  : https://github.com/azwpayne 
# @Time    : 2025/6/15 11:18
# @Abstract:

from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def hello():
    return {'message': 'Hello World!'}
