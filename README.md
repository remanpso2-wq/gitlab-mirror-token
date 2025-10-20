# Mochizuki_Takamasa_internProject01 — 課題① 提出用 README（完全版）

学校向け「連絡帳管理」PoC（課題①）。  
**前登校日のみ提出可**／**同日重複禁止**／**既読は POST** をサーバ側で厳密に担保。  
実装は **Flask + SQLite**。最小UIは `templates/index.html`。

---

## 📦 リポジトリ構成

Mochizuki_Takamasa_internProject01/
├─ app.py # 本体（前登校日バリデーション/重複禁止/既読POST）
├─ templates/
│ └─ index.html # 最小UI（提出フォーム + 一覧）
├─ seed.py # サンプルデータ投入（管理者操作を seed で代替）
├─ .env.example # 環境変数テンプレ（.env は含めない）
├─ .gitignore # .venv/.env/*.db などを除外
├─ requirements.txt # 依存（Flask / Flask-SQLAlchemy）
├─ runtime.txt # python-3.11.x（デプロイ互換用）
├─ Procfile # 任意（gunicorn 起動用）
└─ doc/
├─ presentation.md # 課題①スライド（Marp）
└─ presentation_kadai2.md # 課題②スライド（任意：用意していれば）


> **注意**: Flask は既定で `templates/` を読むため、フォルダ名は複数形です。

---

## ✅ 課題① 仕様への対応（合否の核）

- **前登校日バリデーション**  
  `prev_schoolday_str()` で「土日除外の前営業日」を算出。`/submit` 保存直前に **date==前登校日** を厳密チェック（祝日考慮なし）。

- **同日重複の禁止**  
  `(student_id, date)` の存在チェック＋DB一意制約で再提出をブロック。

- **既読は POST**  
  `/check/<id>` は **POST専用**。UIはフォーム＋ボタン送信（リンク直叩き不可）。

- **閲覧のみ／編集不可**  
  提出済みレコードは一覧で見えるが、編集UIは持たない（既読＝過去記録化）。

- **学年/クラスでの利用（簡易対応）**  
  `Student.grade / class_name` を保持。`/?grade=3&class=A` で簡易フィルタ可能。  
  ※ 今回は PoC のため **権限・ログインは簡略化**（下記の注記参照）。

---

## 🔐 運用ポリシーと注記（提出観点の追記）

- **管理者操作は seed.py で代替**  
  本 PoC では GUI の管理画面を省略し、アカウント／初期データ作成は `seed.py` による投入で代替します。

- **権限の簡略化について**  
  課題①では「生徒が自分の記録のみ閲覧」の要件に対し、本 PoC は **ログイン/権限を簡略化**しています。  
  レビュー用に「単一画面で動作確認可能」とするためで、将来は `flask-login` 等で分離予定です。

- **秘匿情報の扱い**  
  `.env` 実体と SQLite の `*.db` は **コミットしません**。`/.gitignore` 済み。  
  代わりに `.env.example` を同梱しています。

---

## 👤 テストアカウント（seed.py で投入される例）

| 区分   | 氏名       | 備考                   |
|-------|------------|------------------------|
| 生徒   | 望月 孝義  | grade=3, class=A       |
| 生徒   | 佐藤 花子  | grade=3, class=A       |

> `seed.py` 実行で上記と直近のテスト提出データが生成されます。  
> 本 PoC はログインを省略しているため、画面からは全体を確認できます。

---

## 🛠 セットアップ & 起動

### PowerShell
```powershell
cd "$HOME\Desktop\mochizuki_takamasa_internproject01"

# 仮想環境（初回のみ）
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 依存
pip install -r requirements.txt

# 環境変数（必要なら編集）
Copy-Item .env.example .env

# 初期データ投入（任意）
py .\seed.py

# 起動
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run -p 8000
# → http://localhost:8000

cd ~/Desktop/mochizuki_takamasa_internproject01
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
FLASK_APP=app.py FLASK_ENV=development flask run -p 8000

動作確認チェックリスト

画面 / が表示され、フォーム日付が 前登校日 になっている

今日の日付で送信 → 弾かれる（フラッシュ表示）

前登校日で送信 → 一覧に追加される

同じ生徒・同じ日付で再送信 → 重複禁止で弾かれる

行の「既読にする」→ POST で ✅ に変わる

/?grade=3&class=A で フィルタ が効く

🔍 エンドポイント
/	GET	一覧 + 提出フォーム（デフォルトで前登校日を表示）
/submit	POST	前登校日チェック & 同日重複禁止 を満たして保存
/check/<report_id>	POST	既読処理（POSTのみ）

🗃 データモデル（ER 図 / Mermaid）
erDiagram
  STUDENT ||--o{ REPORT : has
  STUDENT {
    int id PK
    string name
    int grade
    string class_name
  }
  REPORT {
    int id PK
    int student_id FK
    string date  "YYYY-MM-DD"
    bool is_checked
    text content
  }

🎛 学年・クラスの使い方（簡易運用）
生徒の grade / class_name は seed で設定（必要なら DB 直接更新でも可）
一覧のクエリで絞り込み：
例）/?grade=3&class=A
片方だけでもOK：/?grade=3

🚀 デプロイ（任意）
runtime.txt: python-3.11.x を指定（例：python-3.11.9）
Procfile: web: gunicorn app:app など
環境変数：SECRET_KEY / DATABASE_URL（未指定は SQLite ローカル）

🧯 トラブルシュート

500 / no such table: student
→ python seed.py を実行（DB作成＋サンプル投入）。
または app.py に @app.before_first_request で db.create_all() を追加。

TemplateNotFound: index.html
→ templates/index.html が存在／スペル／app.py と同階層か確認。
フォルダ名は templates（複数形）。

PowerShell で venv が有効化できない
→ Set-ExecutionPolicy -Scope CurrentUser RemoteSigned を一度実行。

📥 提出前セルフチェック
前登校日以外の提出不可
(student_id, date) 重複不可
既読が POST で反映
templates/index.html あり（UI表示OK）
.env/*.db は コミットしていない（.env.example は含む）
requirements.txt / runtime.txt あり
doc/presentation.md（課題①スライド）あり
README に「seed で管理者操作を代替」「権限簡略化の注記」あり

📝 補足
本 PoC は課題①の主目的（提出ルールの機械化）を最小構成で満たします。
課題②（分析・共有メモ等）は doc/presentation_kadai2.md で説明（実装がある場合）