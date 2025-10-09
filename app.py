from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
import os  # ← ★ これを追加！

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SECRET_KEY'] = 'secret-key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# ==== モデル定義 ====
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'student', 'teacher', 'admin'

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20))
    is_checked = db.Column(db.Boolean, default=False)

# ==== DB初期化 ====
@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()


# ==== 各ルート ====
@app.route('/')
def home():
    return "連絡帳システム（仮）稼働中"

@app.route('/register')
def register():
    return "登録ページ（仮）"

@app.route('/login')
def login():
    return "ログインページ（仮）"

# ==== ★ DB確認ルート ====

@app.route('/check_db')
def check_db():
    import os
    if os.path.exists("diary.db"):
        return "✅ diary.db found!"
    else:
        return "❌ diary.db not found!"


if __name__ == '__main__':
    app.run(debug=True)
