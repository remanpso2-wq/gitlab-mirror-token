# Mochizuki_Takamasa_internProject01 — 課題① 提出用

学校向け「連絡帳管理」PoC（課題①）。  
**前登校日のみ提出可**／**同日重複禁止**／**既読はPOST** をサーバ側で厳密に担保します。  
実装は **Flask + SQLite**。最小UIは `templates/index.html`。

---

## 📦 リポジトリ構成（最小）

Mochizuki_Takamasa_internProject01/
├─ app.py # 本体（前登校日バリデーション/重複禁止/既読POST）
├─ templates/
│ └─ index.html # 最小UI（提出フォームと一覧）
├─ seed.py # サンプルデータ投入（任意）
├─ .env.example # 環境変数テンプレート（.env は含めない）
├─ .gitignore # .venv/.env/*.db などを除外
├─ requirements.txt # 依存（Flask / Flask-SQLAlchemy）
├─ runtime.txt # python-3.11.x（デプロイ互換）
├─ Procfile # （任意）gunicorn起動などのデプロイ向け
├─ README.md # 本ファイル
└─ CHECKLIST.md # 任意。提出前セルフチェック


> **注意**: Flask は既定で `templates/` を読むため、フォルダ名は複数形です。

---

## ✅ 課題①の要件に対する実装ポイント（合否の核）

- **前登校日バリデーション**  
  `prev_schoolday_str()` で「土日除外の前営業日」を算出。`/submit` 保存直前に **date==前登校日** を厳密チェック。  
  ※祝日考慮なし（要件準拠）。

- **同日重複の禁止**  
  `(student_id, date)` の一意制約（アプリロジック＆DB制約）で再提出をブロック。

- **既読は POST でのみ**  
  `/check/<id>` は **POST専用**。UIはリンクではなくフォーム+ボタンで送信。

- **閲覧は可能、改変不可**  
  提出済みレコードは一覧で見えるが、編集UIは持たない（既読＝過去記録化）。

- （任意）**学年/クラスの最小対応**  
  `Student.grade / class_name` を追加済み。`/?grade=3&class=A` で簡易フィルタ可能。

---

## 🛠 セットアップ & 起動（PowerShell想定）

```powershell
# 0) （初回のみ）仮想環境
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 1) 依存インストール
pip install -r requirements.txt

# 2) 環境変数（必要なら値を調整）
Copy-Item .env.example .env

# 3) サンプルデータ投入（任意）
py .\seed.py

# 4) 起動
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run -p 8000
# → http://localhost:8000

Git Bash の場合：
source .venv/Scripts/activate → python seed.py → flask run -p 8000

🧪 動作確認チェックリスト（短時間でOK）

画面 / が表示され、前登校日がフォームの既定日に入っている

前登校日以外の date を入力 → 弾かれる（フラッシュ表示）

同じ生徒・同日で再提出 → 弾かれる（重複禁止）

一覧の「既読にする」→ POST で既読化される

/?grade=3&class=A のようなクエリで簡易フィルタが効く（任意）

🗃 データモデル（簡易ER）
Student(id, name, grade?, class_name?)
Report(id, student_id, content, date(YYYY-MM-DD string), is_checked)
# Unique: (student_id, date)

Unique制約で同日二重登録をロジック & DB 両面で防止

フィルタ用途に grade/class_name を設置（空でも動作可）

🔐 セキュリティ・運用

.env と 実DB はコミットしない

.env.example を配布、評価側は .env を作って起動

SQLite の *.db は .gitignore 済み（instance/ も除外）

フォーム送信は今は最小構成（CSRFは課題②以降で強化想定）

🚀 デプロイ（任意）

runtime.txt は python-3.11.x を指定（例：python-3.11.9）

Procfile がある場合は web: gunicorn app:app などを設定

環境変数：SECRET_KEY / DATABASE_URL（未指定ならローカルSQLite）

🧯 トラブルシュート

テンプレートが見つからない
→ フォルダ名が templates/（複数形）か確認。

ポート競合
→ -p 8000 を別ポートに変更。

Windowsで仮想環境が有効化できない
→ 管理者PowerShell で Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

📥 提出前セルフチェック
templates/index.html が存在し、一覧とフォームが表示される
前登校日以外の提出が不可
(student_id, date) 重複不可
既読が POST で反映
.env/*.db はコミットされていない（.env.example は含む）
requirements.txt / runtime.txt が存在
