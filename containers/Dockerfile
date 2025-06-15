## 阶段1: 基础依赖层
FROM  python:3.11-alpine as base

# 设置工作目录
WORKDIR /app

## 安装系统依赖 (单独分层)
#RUN #apt-get update && \
#    apt-get install -y --no-install-recommends gcc libpq-dev && \
#    rm -rf /var/lib/apt/lists/*

# 阶段2: 依赖安装层 (利用缓存)
FROM base as dependencies

## 安装 Python 依赖 (优先复制 requirements 文件利用缓存)
COPY requirements.txt ./
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

## 阶段3: 应用构建层
FROM dependencies as build

# 复制应用代码 (在依赖之后复制以加速构建)
COPY . ./app

## 阶段4: 生产运行环境
FROM base as production

## 从依赖层复制已安装的包
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

## 从构建层复制应用代码
COPY --from=build /app .
COPY . .
## 暴露端口
EXPOSE 8000

# 运行应用 (使用 Gunicorn 作为示例)
CMD ["gunicorn", "main:app","--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "8","--timeout", "120"]