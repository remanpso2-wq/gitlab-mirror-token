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

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
ROLE_CHOICES = (
("student", "生徒"),
("teacher", "担任"),
("admin", "管理者"),
)
role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
assigned_class = models.CharField(max_length=16, blank=True, null=True)
grade = models.CharField(max_length=16, blank=True, null=True)

from django.db import models
from django.conf import settings


class ContactEntry(models.Model):
student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="entries")
date = models.DateField(auto_now_add=True)
content = models.TextField()
condition = models.CharField(max_length=64, blank=True)
liked = models.BooleanField(default=False)
read_by_teacher = models.BooleanField(default=False)
created_at = models.DateTimeField(auto_now_add=True)

from rest_framework import permissions


class IsOwnerNoEditAfterRead(permissions.BasePermission):
def has_object_permission(self, request, view, obj):
if request.user.role == "student":
if obj.student != request.user:
return False
if obj.read_by_teacher and request.method not in permissions.SAFE_METHODS:
return False
elif request.user.role == "teacher":
return obj.student.assigned_class == request.user.assigned_class
return True

import { useState } from "react";
export default function Login() {
const [email, setEmail] = useState("");
const [password, setPassword] = useState("");
const handleSubmit = (e: React.FormEvent) => {
e.preventDefault();
console.log("Login with", email, password);
};
return (
<div className="flex h-screen items-center justify-center bg-gray-100">
<form onSubmit={handleSubmit} className="bg-white p-8 rounded shadow w-80">
<h1 className="text-xl font-bold mb-4">学校連絡帳ログイン</h1>
<input type="email" value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="メールアドレス" className="w-full mb-2 p-2 border rounded" />
<input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="パスワード" className="w-full mb-4 p-2 border rounded" />
<button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">ログイン</button>
</form>
</div>
);
}

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

stages:
- lint
- test
- build
- deploy


variables:
REGISTRY: registry.gitlab.com/<TAKAMASA MOCHIZUKI>/<Mochizuki_Takamasa_internProject01>
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
- ssh $DEPLOY_USER@$DEPLOY_HOST "cd /srv/contactbook && docker-compose pull && docker-compose up -d"
only:
- main