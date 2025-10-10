from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
import os  # ← ★ これを追加！

app = Flask(__name__)
import os  

# DBファイルをRender環境で確実に保存できるよう絶対パス指定
db_path = os.path.join(os.getcwd(), "diary.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"



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
with app.app_context():
    db.create_all()

# ==== RenderでDBが確実に生成されるようにする ====
def ensure_db_exists():
    import os
    db_path = os.path.join(os.getcwd(), "diary.db")
    if not os.path.exists(db_path):
        print("🟡 diary.db not found — creating new database...")
        with app.app_context():
            db.create_all()
        print("✅ diary.db successfully created!")

ensure_db_exists()

# ==== 各ルート ====
@app.route('/')
def home():
    return "連絡帳システム（仮）稼働中"

@app.route('/register')
def register():
    return "登録ページ（仮)"

@app.route('/login')
def login():
    return "ログインページ（仮)"

# ==== ★ DB確認ルート ====

@app.route('/check_db')
def check_db():
    import os
    if os.path.exists("diary.db"):
        return "✅ diary.db found!"
    else:
        return "❌ diary.db not found!"

# ==== テストユーザー自動追加 ====
@app.before_first_request
def create_test_users():
    from your_model_file import Student  # Studentモデルの場所に応じて変更してね

    test_user = Student(id='test_student', name='テスト学生', password='1234')
    teacher_user = Student(id='teacher', name='担任ユーザー', password='abcd')

    # すでに存在しない場合だけ追加
    if not Student.query.filter_by(id='test_student').first():
        db.session.add(test_user)
    if not Student.query.filter_by(id='teacher').first():
        db.session.add(teacher_user)
    db.session.commit()
    print("✅ テスト用アカウントを初期化しました！")



if __name__ == '__main__':
    app.run(debug=True)

python # Updated at 2025-10-09 for Render fix 　