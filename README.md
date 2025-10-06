# Mochizuki_Takamasa_internProject01



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://intern.jpt.jgc.com/takamasa.mochizuki/mochizuki_takamasa_internproject01.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://intern.jpt.jgc.com/takamasa.mochizuki/mochizuki_takamasa_internproject01/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

school-contactbook/
├─ frontend/ # React (TypeScript)
│ ├─ public/
│ ├─ src/
│ │ ├─ components/
│ │ ├─ pages/
│ │ ├─ api/
│ │ └─ index.tsx
│ ├─ package.json
│ └─ tsconfig.json
├─ backend/ # Django
│ ├─ contacts/ # Django アプリ (連絡先管理)
│ ├─ users/ # Django アプリ (ユーザ認証・権限)
│ ├─ notifications/ # 一斉連絡用アプリ
│ ├─ conditions/ # 生徒コンディション管理アプリ
│ ├─ config/ # settings, urls
│ ├─ requirements.txt
│ └─ manage.py
├─ infra/
│ ├─ Dockerfile.frontend
│ ├─ Dockerfile.backend
│ └─ docker-compose.yml
├─ .gitlab-ci.yml
├─ README.md
└─ LICENSE

conditions/models.py

from django.db import models
from contacts.models import Contact


class Condition(models.Model):
contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="conditions")
date = models.DateField(auto_now_add=True)
status = models.CharField(max_length=32) # 例: "元気", "疲れ気味", "体調不良"
like_stamp = models.BooleanField(default=False) # イイネスタンプが押されたか


def auto_like(self):
if self.status == "元気":
self.like_stamp = True
elif self.status == "疲れ気味":
self.like_stamp = True # 応援の意味で
else:
self.like_stamp = False
self.save()

# conditions/tasks.py
from .models import Condition


def auto_assign_like():
for condition in Condition.objects.filter(like_stamp=False):
condition.auto_like()

src/pages/ConditionList.tsx

import { useEffect, useState } from "react";


interface Condition {
id: number;
contact: number;
date: string;
status: string;
like_stamp: boolean;
}


export default function ConditionList() {
const [conditions, setConditions] = useState<Condition[]>([]);


useEffect(() => {
fetch("/api/conditions/")
.then((res) => res.json())
.then((data) => setConditions(data));
}, []);


return (
<div className="p-4">
<h1 className="text-2xl mb-4">生徒コンディション</h1>
<table className="w-full border">
<thead>
<tr className="bg-gray-200">
<th className="p-2 border">日付</th>
<th className="p-2 border">状態</th>
<th className="p-2 border">イイネ</th>
</tr>
</thead>
<tbody>
{conditions.map((c) => (
<tr key={c.id}>
<td className="border p-2">{c.date}</td>
<td className="border p-2">{c.status}</td>
<td className="border p-2">{c.like_stamp ? "👍" : ""}</td>
</tr>
))}
</tbody>
</table>
</div>
);
}

.gitlab/issue_templates/feature.md

# 学校向け 連絡帳管理システム

Microsoft Edge を主要ブラウザに想定し、GitLab 上で開発・運用する学校用の連絡帳管理システムです。

## 主な機能
- 連絡先管理 (CRUD)
- ユーザ認証・権限管理 (管理者 / 教員 / 保護者)
- CSV インポート／エクスポート
- 一斉連絡（メール通知）
- 生徒のコンディションに基づく 👍 スタンプ自動付与

## 技術スタック
- Frontend: React (TypeScript) + Tailwind CSS
- Backend: Django REST Framework (Python)
- DB: PostgreSQL
- 認証: JWT (djangorestframework-simplejwt)
- CI/CD: GitLab CI + Docker

## 開発手順
```bash
# backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# frontend
cd frontend
npm install
npm run dev

---

## 2. GitLab Issue テンプレート（拡充）

### `.gitlab/issue_templates/feature.md`

```markdown
## 概要
(新機能の目的や背景)

## 実装内容
- [ ] バックエンド API
- [ ] フロントエンド UI
- [ ] テストコード
- [ ] ドキュメント更新

## 受け入れ基準
- ユーザが操作できる UI がある
- バックエンド API と連携済み
- CI/CD でテストが通る

stages:
  - lint
  - test
  - build
  - deploy

variables:
  REGISTRY: registry.gitlab.com/<MochizukiTakamasa>/<Mochizuki_Takamasa_internProject01>
  FRONTEND_IMAGE: $REGISTRY/frontend
  BACKEND_IMAGE: $REGISTRY/backend

lint_frontend:
  stage: lint
  image: node:20
  script:
    - cd frontend
    - npm ci
    - npm run lint

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

deploy:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Deploying to production server..."
    # 例: SSH でサーバにログインして docker-compose pull/up を実行
    - ssh $DEPLOY_USER@$DEPLOY_HOST "cd /srv/contactbook && docker-compose pull && docker-compose up -d"
  only:
    - main