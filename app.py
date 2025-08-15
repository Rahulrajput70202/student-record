from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student, Grade

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

# Initialize db with app
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        new_student = Student(name=name, roll_number=roll_number)
        db.session.add(new_student)
        db.session.commit()
        flash("Student added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/student/<int:id>')
def student_detail(id):
    student = Student.query.get_or_404(id)
    return render_template('student_detail.html', student=student)

@app.route('/student/<int:id>/add_grade', methods=['POST'])
def add_grade(id):
    subject = request.form['subject']
    score = float(request.form['score'])
    new_grade = Grade(subject=subject, score=score, student_id=id)
    db.session.add(new_grade)
    db.session.commit()
    flash("Grade added successfully!", "success")
    return redirect(url_for('student_detail', id=id))

@app.route('/student/<int:id>/edit', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.roll_number = request.form['roll_number']
        db.session.commit()
        flash("Student updated successfully!", "success")
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)

@app.route('/student/<int:id>/delete', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
