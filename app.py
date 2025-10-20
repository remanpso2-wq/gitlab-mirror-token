from datetime import datetime, timedelta
import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

# =====================
# 設定
# =====================
DB_URL = os.getenv("DATABASE_URL", "sqlite:///diary.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
db = SQLAlchemy(app)

# =====================
# モデル
# =====================
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    # 課題①の“学年/クラスで利用”の最低限対応（任意入力）
    grade = db.Column(db.Integer, nullable=True)
    class_name = db.Column(db.String(20), nullable=True)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # 課題①の実装に合わせて日付は "YYYY-MM-DD" の文字列で保持
    date = db.Column(db.String(10), nullable=False)
    is_checked = db.Column(db.Boolean, default=False, nullable=False)

    student = db.relationship("Student", backref="reports")

    # 同日重複禁止
    __table_args__ = (UniqueConstraint("student_id", "date", name="uix_student_date"),)


# =====================
# ユーティリティ
# =====================
def prev_schoolday_str(base_dt: datetime) -> str:
    """祝日考慮なしで“前登校日”(土日除外)を返す"""
    d = base_dt.date() - timedelta(days=1)
    while d.weekday() >= 5:  # 5:Sat, 6:Sun
        d -= timedelta(days=1)
    return d.strftime("%Y-%m-%d")


def get_or_create_student(name: str) -> Student:
    s = Student.query.filter_by(name=name).first()
    if not s:
        s = Student(name=name)
        db.session.add(s)
        db.session.commit()
    return s


# =====================
# ルート
# =====================
@app.route("/")
def index():
    """一覧 + 登録フォーム（前登校日デフォルト）"""
    expected = prev_schoolday_str(datetime.now())

    # 学年/クラスの簡易絞り込み（?grade=3&class=A）
    q = Student.query
    q_grade = request.args.get("grade", type=int)
    q_class = request.args.get("class")
    if q_grade:
        q = q.filter(Student.grade == q_grade)
    if q_class:
        q = q.filter(Student.class_name == q_class)

    students = q.order_by(Student.name.asc()).all()
    # 直近の提出一覧（新しい順）
    reports = Report.query.order_by(Report.date.desc(), Report.id.desc()).limit(100).all()
    return render_template("index.html",
                           expected_date=expected, students=students, reports=reports)


@app.route("/submit", methods=["POST"])
def submit_report():
    """提出：前登校日だけ受付 / 同日重複禁止"""
    student_name = (request.form.get("student_name") or "").strip()
    content = (request.form.get("content") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    if not student_name or not content or not date_str:
        flash("必須項目が不足しています")
        return redirect(url_for("index"))

    # 1) 前登校日チェック
    expected = prev_schoolday_str(datetime.now())
    if date_str != expected:
        flash(f"提出日は前登校日（{expected}）のみです")
        return redirect(url_for("index"))

    # 2) 同日重複禁止
    student = get_or_create_student(student_name)
    exists = Report.query.filter_by(student_id=student.id, date=date_str).first()
    if exists:
        flash("同日の提出は完了済みです")
        return redirect(url_for("index"))

    # 登録
    r = Report(student_id=student.id, content=content, date=date_str, is_checked=False)
    db.session.add(r)
    db.session.commit()
    flash("提出を登録しました")
    return redirect(url_for("index"))


@app.route("/check/<int:report_id>", methods=["POST"])
def check_report(report_id: int):
    """既読は POST のみ"""
    r = Report.query.get_or_404(report_id)
    if not r.is_checked:
        r.is_checked = True
        db.session.commit()
        flash("既読にしました")
    return redirect(url_for("index"))


# =====================
# エントリポイント
# =====================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
