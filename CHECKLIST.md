# ✅ 課題① 提出チェックリスト（Intern Flask App）

## 📁 基本情報
- プロジェクト名：intern-flask-app  
- 開発者：望月 孝真（Takamasa Mochizuki）  
- フレームワーク：Flask (Python 3)  
- データベース：SQLite  
- デプロイ環境：Render  
- リポジトリ：`https://gitlab.com/xxxxx/mochizuki_takamasa_internproject01`

---

## 🔧 機能実装チェックリスト

| 項目 | 内容 | 状態 |
|------|------|------|
| ユーザー登録 | 学生ID・氏名による新規登録ができる | ✅ |
| ログイン・ログアウト | 認証機能が実装されている | ✅ |
| 日報作成・一覧表示 | 日報の投稿・閲覧が可能 | ✅ |
| データ永続化 | SQLiteにデータが保存される | ✅ |
| チェック機能 | 担任が日報に既読チェックをつけられる | ✅ |
| 平日提出制御 | 土日祝日を除外して提出制御が動作する | ✅ |

---

## 📊 データベース構造

| テーブル名 | 説明 |
|------------|------|
| `student` | 学生ID・氏名・パスワードなどを管理 |
| `report`  | 日報内容、作成日、チェック状態を保存 |

---

## 🧪 テスト用アカウント情報

| 役割 | ID | パスワード |
|------|----|------------|
| 学生アカウント | test_student | 1234 |
| 担任アカウント | teacher | abcd |

---

## 🌐 デプロイ環境情報

- URL: [https://intern-flask-app.onrender.com](https://intern-flask-app.onrender.com)  
- 確認手順：
  1. 上記URLにアクセス  
  2. ログインページが表示されることを確認  
  3. テスト用アカウントでログイン  
  4. 日報作成・一覧表示・チェック機能の動作を確認  

---

## 🛠️ デプロイ手順（再現可能性）

```bash
# 環境構築
pip install -r requirements.txt

# サーバー起動（ローカル開発用）
python app.py

# GitLabへpush
git add .
git commit -m "final: 提出用バージョン"
git push origin main

# Render側設定
Environment：Python 3
Build Command：pip install -r requirements.txt
Start Command：gunicorn app:app
