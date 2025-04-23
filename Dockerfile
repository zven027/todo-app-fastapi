# ベースイメージ（軽量なPython環境）
FROM python:3.10-slim

# 作業ディレクトリの設定
WORKDIR /app

# プロジェクトファイルをコピー
COPY . /app

# パッケージのインストール
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 本番用のFastAPIアプリ起動コマンド（ポート8000固定）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]