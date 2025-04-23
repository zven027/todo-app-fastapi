完璧です！では、さらに洗練された実務レベルの README に仕上げます。以下は、GitHub 上のポートフォリオとして使えるように整理した完成版です：

⸻

📝 ToDoアプリ（FastAPI + SQLModel）

FastAPI・SQLModel・Jinja2 を活用した拡張性の高いタスク管理アプリです。
タスクの追加・編集・完了状態の切替・タグ付け・期限設定など、業務でも活用可能な機能を備えています。

A clean and extendable ToDo application built with FastAPI, SQLModel, and Jinja2.

⸻

🌐 デプロイ済みアプリ（公開URL）

🔗 https://todo-app-fastapi-production.up.railway.app
	•	Railway にてクラウドホスティング
	•	GitHub Actions による CI/CD 対応
→ main ブランチへの push で自動デプロイが行われます。

⸻

🚀 本番環境デプロイ（AWS EC2 × Docker）

Docker を活用し、AWS EC2 上にアプリを構築・公開しています。

🔧 セットアップ手順（EC2）

# 1. Docker イメージをビルド
docker build -t todo-app .

# 2. コンテナを起動（ポート8000をバインド）
docker run -d -p 8000:8000 --env-file .env todo-app

🔐 .env ファイルには、以下のような接続情報を記述します：

DATABASE_URL=postgresql://<ユーザー名>:<パスワード>@<DBエンドポイント>:5432/<DB名>?sslmode=require

※ EC2 ⇔ RDS 接続のため、セキュリティグループの設定にて ポート 5432 を開放 しておく必要があります。

⸻

🛠️ 技術スタック
	•	Python 3.10
	•	FastAPI（軽量な Web フレームワーク）
	•	SQLModel（SQLAlchemy + Pydantic の統合 ORM）
	•	Jinja2（テンプレートエンジン）
	•	SQLite / PostgreSQL（環境に応じて切替）
	•	GitHub Actions（CI/CD 自動化）
	•	Railway / AWS EC2（本番環境）

⸻

✅ 主な機能
	•	タスクの新規作成・削除・編集（UI + API）
	•	タグ付け機能（多対多リレーション）
	•	完了状態の ON/OFF 切替
	•	タグ・状態別のフィルター表示
	•	タスクの期限（due_date）設定対応

⸻

## 📸 スクリーンショット

| メイン画面 | 絞り込み機能 | 編集画面 |
|------------|--------------|----------|
| ![main](./screenshot_main.png) | ![filtered](./screenshot_filtered.png) | ![edit](./screenshot_edit.png) |

⸻

📁 ディレクトリ構成（抜粋）

todo-app-fastapi/
├── main.py              # アプリ起動エントリ
├── database.py          # DB接続処理
├── crud.py              # DB操作関数群
├── models.py            # SQLModel の定義
├── init_db.py           # 初回DB作成用スクリプト
├── templates/           # Jinja2 HTML テンプレート
├── Dockerfile           # EC2用のDocker定義
├── Dockerfile.railway   # Railway 用のDocker定義
├── docker-compose.yml   # ローカル開発用コンテナ構成
├── .env                 # 環境変数（DATABASE_URLなど）
└── README.md



⸻

📄 ライセンス

MIT License

⸻

🚀 CI/CD Deploy Test Wed Apr 23 22:14:09 JST 2025
