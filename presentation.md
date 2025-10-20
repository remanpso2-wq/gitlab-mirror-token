---
marp: true
title: 学校連絡帳管理 PoC — 課題①
description: 前登校日バリデーション / 同日重複禁止 / 既読はPOST / 学年・クラス対応（簡易）
paginate: true
theme: default
class: lead
---

# 学校連絡帳管理 PoC（課題①）
**前登校日だけ提出可 / 同日重複禁止 / 既読はPOST**  
実装：Flask + SQLite  
---

## 課題① 要件（抜粋）
- 学年・クラスごとに利用できること  
- 生徒は**前登校日**の内容のみ登録（祝日考慮なし）  
- 担任は記録を確認し**既読処理**できる（編集不可）  
- 生徒は自分の過去記録を**閲覧のみ**可能  
- ユーザー管理者はアカウント作成/割当（PoCでは seed で代替）  
※詳細は配布資料の「課題１の仕様」を参照。 :contentReference[oaicite:0]{index=0}

---

## 本PoCの方針
- まずは**ルールの機械化**（提出ルールをサーバで強制）  
- UIは最小構成で、**確実な動作**と**簡単な運用**を優先  
- 課題②で拡張（分析・共有・UX強化）を見据える

---

## アーキテクチャ（最小）
- **Backend**: Flask + Flask-SQLAlchemy  
- **DB**: SQLite（ローカル自動生成。実DBはリポに含めない）  
- **Template**: `templates/index.html`（提出フォーム + 一覧）  
- **Seed**: `seed.py`（テストユーザー/レコード投入）

---

## データモデル（簡易ER）
- `grade` / `class_name` により学年・クラス単位の利用が可能（簡易）  
- 一覧は `/?grade=3&class=A` で絞り込み

---

## 主要エンドポイント
| ルート | メソッド | 役割 |
|---|---|---|
| `/` | GET | 一覧 + 提出フォーム（デフォルトで**前登校日**を表示） |
| `/submit` | POST | **前登校日チェック** & **同日重複禁止**を満たして保存 |
| `/check/<id>` | POST | **既読処理（POSTのみ）** |

---

## ルール実装（サーバ側）
**1) 前登校日バリデーション**  
```python
def prev_schoolday_str(now):
    d = now.date() - timedelta(days=1)
    while d.weekday() >= 5:  # 土日除外、祝日考慮なし
        d -= timedelta(days=1)
    return d.strftime("%Y-%m-%d")
2) 同日重複禁止

アプリ: Report.query.filter_by(student_id, date).first() で事前チェック

DB: UNIQUE(student_id, date) 制約

3) 既読は POST

/check/<id> はフォームから POST 送信のみを許可

---

画面ダイジェスト（最小UI）

フォーム：学生名 / 日付（前登校日）/ 内容

一覧：最新提出から表示、既読は✅、未読は❌

行の「既読にする」ボタン = POST ハンドラ発火

---

デモ台本（60秒）

/ を表示 → 右上の前登校日が既定値

わざと当日で投稿 → エラーフラッシュ（弾かれる）

前登校日に直して投稿 → 一覧に反映

同じ生徒・同日で再投稿 → 重複禁止で弾かれる

「既読にする」→ POST で ✅ に変化

/?grade=3&class=A でクラス絞り込み（任意）デモ台本（60秒）

/ を表示 → 右上の前登校日が既定値

わざと当日で投稿 → エラーフラッシュ（弾かれる）

前登校日に直して投稿 → 一覧に反映

同じ生徒・同日で再投稿 → 重複禁止で弾かれる

「既読にする」→ POST で ✅ に変化

/?grade=3&class=A でクラス絞り込み（任意）

pip install -r requirements.txt
cp .env.example .env    # 値は必要に応じ編集
python seed.py          # 任意
flask run -p 8000       # http://localhost:8000

.env / 実DB（*.db）はコミットしない

runtime.txt: python-3.11.x

---

テスト観点（審査ポイント）

前登校日以外は登録不可

(student_id, date) の二重登録不可

既読処理はPOSTのみ

過去記録は閲覧のみ（編集UIなし）

---

まとめ / 課題②への課題

課題①で提出ルールの自動化を完了

課題②では、週次分析、共有メモ、通知、権限強化へ拡張予定

例：提出率の可視化、低スコア連続アラート、学年会議向け共有

