📝 ToDoアプリ（FastAPI + SQLModel）

FastAPI・SQLModel・Jinja2 を活用した、シンプルかつ拡張性の高いタスク管理アプリです。  
タスクの追加・編集・完了状態の切り替え、タグ付け、期限設定など、業務や個人利用に幅広く対応可能です。

> A clean, maintainable, and extensible ToDo application built with FastAPI, SQLModel, and Jinja2.

---

🌐 公開中のアプリケーション

🚀 Railway 版（開発・検証用途）
🔗 https://todo-app-fastapi-production.up.railway.app  
- Railway によるクラウドホスティング  
- GitHub Actions による CI/CD 自動デプロイ対応

🛡 本番環境版（独自ドメイン × SSL 対応）
🔗 https://zewei.online  
- AWS EC2 × Docker による運用  
- Let’s Encrypt による常時SSL（HTTPS）化  
- `main` ブランチへの push で自動デプロイ（CI/CD）

---

⚙️ 本番環境構成（AWS EC2 × Docker）

Docker を用いてアプリケーションをコンテナ化し、EC2 上で稼働させています。

🔧 セットアップ手順（EC2）

```bash

# 1. Docker イメージをビルド
docker build -t todo-app .

# 2. コンテナを起動（ポート8000をバインド）
docker run -d -p 8000:8000 --env-file .env todo-app

```

DATABASE_URL=postgresql://<ユーザー名>:<パスワード>@<DBエンドポイント>:5432/<DB名>?sslmode=require

※ EC2 ⇔ RDS 接続のため、セキュリティグループの設定にて ポート 5432 を開放 しておく必要があります。

⸻

🛠️ 使用技術スタック
	•	Python 3.10
	•	FastAPI：モダンな非同期Webフレームワーク
	•	SQLModel：Pydantic + SQLAlchemy の融合ORM
	•	Jinja2：軽量テンプレートエンジン
	•	SQLite / PostgreSQL：開発・本番で切替可能
	•	Docker / docker-compose：環境構築の自動化
	•	GitHub Actions：CI/CD自動デプロイ
	•	Railway / AWS EC2：クラウドデプロイ環境
	•	Let’s Encrypt：無料SSL証明書（HTTPS対応）


⸻

✅ 主な機能
	•	タスクの作成・編集・削除（UI / API 両対応）
	•	タグ機能（多対多リレーション）
	•	完了状態の切り替え（ON/OFF）
	•	タグ／状態による絞り込み表示
	•	期限（due_date）の設定
	•	Swagger UI による API 自動ドキュメント

⸻

## 📸 スクリーンショット

| メイン画面 | 絞り込み機能 | 編集画面 |
|------------|--------------|----------|
| ![main](./screenshot_main.png) | ![filtered](./screenshot_filtered.png) | ![edit](./screenshot_edit.png) |

⸻

📁 ディレクトリ構成（抜粋）

todo-app-fastapi/
├── main.py              # アプリ起動エントリポイント
├── database.py          # DB接続定義
├── crud.py              # DB操作関数群
├── models.py            # SQLModelスキーマ定義
├── init_db.py           # 初期DB生成スクリプト
├── templates/           # Jinja2テンプレート（UI）
├── Dockerfile           # EC2 用 Docker ビルド設定
├── Dockerfile.railway   # Railway 用ビルド設定
├── docker-compose.yml   # ローカル開発用構成
├── .env                 # 環境変数設定ファイル
└── README.md            # このファイル



⸻

📄 ライセンス

MIT License

⸻

