from datetime import date, timedelta
from app import db, Student, Report, prev_schoolday_str, app

with app.app_context():
    db.create_all()
    # 学生
    s1 = Student.query.filter_by(name="望月 孝義").first() or Student(name="望月 孝義", grade=3, class_name="A")
    s2 = Student.query.filter_by(name="佐藤 花子").first() or Student(name="佐藤 花子", grade=3, class_name="A")
    db.session.add_all([s1, s2]); db.session.commit()

    today = date.today()
    for s in (s1, s2):
        for i in range(1, 6):
            d = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            if not Report.query.filter_by(student_id=s.id, date=d).first():
                db.session.add(Report(student_id=s.id, content=f"{s.name} の記録 {d}", date=d, is_checked=(i%2==0)))
    db.session.commit()
    print("Seeded.")
