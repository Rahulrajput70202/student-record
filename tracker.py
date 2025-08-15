# tracker.py
"""
Student Performance Tracker - Core OOP + Database Layer
- Defines Student and StudentTracker classes as required.
- Uses SQLAlchemy with SQLite for persistence.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from statistics import mean

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# --- Lightweight app+db factory for reuse in CLI or Flask ---
db = SQLAlchemy()

def create_db_app(database_url: str = "sqlite:///students.db") -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

# --- DB Models ---
class StudentModel(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    grades = db.relationship("GradeModel", backref="student", cascade="all, delete-orphan")

class GradeModel(db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

# --- OOP Classes as per spec ---
@dataclass
class Student:
    name: str
    roll_number: str
    grades: Dict[str, float]

    def add_grade(self, subject: str, score: float) -> None:
        if not (0 <= score <= 100):
            raise ValueError("Grade must be between 0 and 100.")
        self.grades[subject] = float(score)

    def average(self) -> float:
        return mean(self.grades.values()) if self.grades else 0.0

    def info(self) -> Dict:
        return {"name": self.name, "roll_number": self.roll_number, "grades": self.grades, "average": self.average()}

class StudentTracker:
    """Facade around the DB providing required methods and using OOP Student."""
    def __init__(self, database_url: str = "sqlite:///students.db"):
        self.app = create_db_app(database_url)
        with self.app.app_context():
            db.create_all()

    # --- Helper ---
    def _get_student_model(self, roll_number: str) -> Optional[StudentModel]:
        with self.app.app_context():
            return StudentModel.query.filter_by(roll_number=roll_number).first()

    def is_roll_unique(self, roll_number: str) -> bool:
        return self._get_student_model(roll_number) is None

    # --- Core Methods ---
    def add_student(self, name: str, roll_number: str) -> Student:
        with self.app.app_context():
            if not self.is_roll_unique(roll_number):
                raise ValueError("Roll number already exists.")
            sm = StudentModel(name=name.strip(), roll_number=roll_number.strip())
            db.session.add(sm)
            db.session.commit()
            return Student(name=sm.name, roll_number=sm.roll_number, grades={})

    def add_grades(self, roll_number: str, grades: Dict[str, float]) -> Student:
        with self.app.app_context():
            sm = self._get_student_model(roll_number)
            if not sm:
                raise LookupError("Student not found.")
            # upsert grades
            for subject, score in grades.items():
                if not (0 <= float(score) <= 100):
                    raise ValueError("Grade must be between 0 and 100.")
                g = GradeModel.query.filter_by(student_id=sm.id, subject=subject).first()
                if g:
                    g.score = float(score)
                else:
                    db.session.add(GradeModel(subject=subject, score=float(score), student_id=sm.id))
            db.session.commit()
            return self.view_student_details(roll_number)

    def view_student_details(self, roll_number: str) -> Student:
        with self.app.app_context():
            sm = self._get_student_model(roll_number)
            if not sm:
                raise LookupError("Student not found.")
            grades = {g.subject: g.score for g in sm.grades}
            return Student(name=sm.name, roll_number=sm.roll_number, grades=grades)

    def calculate_average(self, roll_number: str) -> float:
        return self.view_student_details(roll_number).average()

    # --- Bonus ---
    def subject_topper(self, subject: str) -> Optional[Tuple[str, str, float]]:
        """Return (name, roll_number, score) for the topper in a subject."""
        with self.app.app_context():
            rows = (
                db.session.query(StudentModel.name, StudentModel.roll_number, GradeModel.score)
                .join(GradeModel, StudentModel.id == GradeModel.student_id)
                .filter(GradeModel.subject == subject)
                .order_by(GradeModel.score.desc())
                .all()
            )
            return rows[0] if rows else None

    def class_average_for_subject(self, subject: str) -> Optional[float]:
        with self.app.app_context():
            scores = [r[0] for r in db.session.query(GradeModel.score).filter_by(subject=subject).all()]
            return mean(scores) if scores else None

    # --- Export / Backup ---
    def export_to_txt(self, path: str = "backup_students.txt") -> str:
        with self.app.app_context():
            students = StudentModel.query.all()
            lines = []
            for sm in students:
                grades = {g.subject: g.score for g in sm.grades}
                s = Student(name=sm.name, roll_number=sm.roll_number, grades=grades)
                lines.append(json.dumps(s.info(), ensure_ascii=False))
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            return path
