FROM python:3.11.2

ENV PYTHONUNBUFFERED 1

# 必要なパッケージをインストール
RUN mkdir -p /root/workspace
COPY containers/requirements.txt /root/workspace/requirements.txt


WORKDIR /root/workspace


# パッケージのインストール
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install --no-cache-dir -r requirements.txt

# プロジェクトのソースコードをコンテナにコピー
COPY src/uniqa /root/workspace/src/uniqa

EXPOSE 8000


