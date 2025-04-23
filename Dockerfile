# ベースイメージ
FROM python:3.10-slim

# 作業ディレクトリ
WORKDIR /app

# ファイルをコピー
COPY . /app

# 依存関係をインストール
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ポートは Railway の環境変数 PORT を使う
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}