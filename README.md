# Mochizuki_Takamasa_internProject01

## 🧾 課題①：Flask × SQLite × Render（基本構成）
🎯 課題概要
Flaskを用いた簡易的なWebアプリを構築し
SQLiteデータベースの自動生成とRender環境でのデプロイを実現しました。
学校向け「連絡帳システム（PoC版）」です。  
生徒・担任・管理者の3ロールで連携し、  
平日のみ記録を提出・確認できるWebアプリケーションを開発します。

🧩 プロジェクト情報
項目	内容
開発者	TAKAMASA MOCHIZUKI
環境	Python 3.11 / Flask
データベース	SQLite（diary.db）
デプロイ環境	Render（Free Tier）
リポジトリ管理	GitLab
動作確認日	2025/10/09

Mochizuki_Takamasa_internProject01/
├─ app.py                # Flaskアプリ本体
├─ requirements.txt      # 依存パッケージ定義
├─ runtime.txt           # Pythonランタイム指定
├─ Procfile              # Renderデプロイ用設定
└─ README.md             # プロジェクト概要


---
##🧩 リポジトリ構成
#school-contactbook/
├─ frontend/                # React (TypeScript)
│  ├─ public/
│  ├─ src/
│  │  ├─ components/
│  │  ├─ pages/
│  │  │  ├─ Login.tsx
│  │  │  └─ ContactList.tsx
│  │  ├─ api/
│  │  └─ index.tsx
│  ├─ package.json
│  └─ tsconfig.json
│
├─ backend/                 # Django REST Framework
│  ├─ contacts/             # 連絡帳アプリ
│  ├─ users/                # 認証・権限管理
│  ├─ config/               # 設定
│  ├─ requirements.txt
│  └─ manage.py
│
├─ infra/                   # Docker・CI設定
│  ├─ Dockerfile.frontend
│  ├─ Dockerfile.backend
│  └─ docker-compose.yml
│
├─ .gitlab-ci.yml           # GitLab CI/CDパイプライン
├─ README.md
└─ LICENSE


---
##⚙️ 技術スタック
##区分	使用技術
##フロントエンド	React + TypeScript + Tailwind CSS
##バックエンド	Django + Django REST Framework
##データベース	PostgreSQL
##認証方式	JWT（JSON Web Token）
##CI/CD	GitLab CI + Docker
##休日判定	jpholiday（日本の祝日判定ライブラリ）

##🧩 Django モデル例
from django.contrib.auth.models import AbstractUser
from django.db import models
import jpholiday
from django.core.exceptions import ValidationError

📦 使用パッケージ（requirements.txt）
Flask
Flask-SQLAlchemy
Flask-Login
Flask-Bcrypt


class User(AbstractUser):
    ROLE_CHOICES = (
        ("student", "生徒"),
        ("teacher", "担任"),
        ("admin", "管理者"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    assigned_class = models.CharField(max_length=16, blank=True, null=True)
    grade = models.CharField(max_length=16, blank=True, null=True)


class ContactEntry(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    condition = models.CharField(max_length=64, blank=True)
    liked = models.BooleanField(default=False)
    read_by_teacher = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # 土日祝日は提出不可
        if self.date.weekday() >= 5 or jpholiday.is_holiday(self.date):
            raise ValidationError("土日祝日は提出できません")

##🧩 React ページ例
import { useEffect, useState } from "react";

interface ContactEntry {
  id: number;
  student_name: string;
  date: string;
  content: string;
  condition: string;
  liked: boolean;
  read_by_teacher: boolean;
}

export default function ContactList() {
  const [entries, setEntries] = useState<ContactEntry[]>([]);

  useEffect(() => {
    fetch("/api/contactentries/")
      .then(res => res.json())
      .then(data => setEntries(data));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl mb-4">連絡帳一覧</h1>
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-200">
            <th className="p-2 border">日付</th>
            <th className="p-2 border">生徒名</th>
            <th className="p-2 border">内容</th>
            <th className="p-2 border">状態</th>
            <th className="p-2 border">👍</th>
            <th className="p-2 border">既読</th>
          </tr>
        </thead>
        <tbody>
          {entries.map(e => (
            <tr key={e.id}>
              <td className="border p-2">{e.date}</td>
              <td className="border p-2">{e.student_name}</td>
              <td className="border p-2">{e.content}</td>
              <td className="border p-2">{e.condition}</td>
              <td className="border p-2">{e.liked ? "👍" : ""}</td>
              <td className="border p-2">{e.read_by_teacher ? "✅" : ""}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
##🧪 CI/CD 設定（.gitlab-ci.yml）
stages:
  - lint
  - test
  - build
  - deploy

variables:
  REGISTRY: registry.gitlab.com/<USERNAME>/<PROJECT>
  FRONTEND_IMAGE: $REGISTRY/frontend
  BACKEND_IMAGE: $REGISTRY/backend

lint_backend:
  stage: lint
  image: python:3.11
  script:
    - cd backend
    - pip install -r requirements.txt
    - flake8

test_backend:
  stage: test
  image: python:3.11
  script:
    - cd backend
    - pip install -r requirements.txt
    - pytest

build_and_push:
  stage: build
  image: docker:24
  services:
    - docker:dind
  script:
    - docker build -t $FRONTEND_IMAGE:$CI_COMMIT_SHA -f infra/Dockerfile.frontend .
    - docker build -t $BACKEND_IMAGE:$CI_COMMIT_SHA -f infra/Dockerfile.backend .
    - docker push $FRONTEND_IMAGE:$CI_COMMIT_SHA
    - docker push $BACKEND_IMAGE:$CI_COMMIT_SHA
  only:
    - main

##🧭 開発ルール・受け入れ基準
##生徒が自分の記録だけ閲覧・提出できる（平日のみ）
##担任が担当クラスの提出状況を確認できる
##担任が既読処理を行える
##管理者がユーザー作成・クラス割当できる
##CI/CD パイプラインでテストが通ること

📊 テスト用アカウント

- 学生用: ID = test_student / PW = 1234
- 担任用: ID = teacher / PW = abcd


🏁 まとめ

本課題では、

FlaskでのWebアプリ構築

SQLiteデータベースの自動生成

GitLab連携とRenderデプロイ

を通じて、基本的なWebアプリ開発の流れを理解しました。
