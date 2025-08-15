# Student Performance Tracker

A complete Python + Flask project to track students, record subject-wise grades, compute averages, and generate simple reports. Includes:
- **OOP layer** (`Student`, `StudentTracker`) using **SQLite** via SQLAlchemy.
- **CLI** app (`cli.py`) with a menu-driven interface.
- **Web app** (`app.py` + Jinja templates) for a friendly UI.
- **Deployment** files for Heroku/Render (Procfile, requirements.txt).

## 1) Quick Start (Local)

```bash
# 1. Create and activate a virtualenv (recommended)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the web app (http://127.0.0.1:5000)
python app.py

# OR run the CLI
python cli.py
```

A `students.db` SQLite file will be created automatically on first run.

## 2) Project Structure

```
student-performance-tracker/
├─ app.py                 # Flask web app
├─ cli.py                 # Menu-driven CLI
├─ tracker.py             # OOP + DB layer (Student, StudentTracker)
├─ requirements.txt
├─ Procfile               # For Heroku/Render
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ student_details.html
│  └─ subject_report.html
└─ static/
   └─ styles.css
```

## 3) Core Features

- **Add Students** (name, roll number – roll must be unique)
- **Add/Update Grades** per subject (0–100 only)
- **View Student Details** (all grades + average)
- **Calculate Average** per student
- **Subject-wise Topper** (bonus)
- **Class Average for a Subject** (bonus)
- **Backup to Text File** (bonus)

All rules validated with clear error messages.

## 4) REST & Routes (Web)

- `GET /` – list students + form to add
- `POST /students/add` – add a student
- `GET /students/<roll>` – details page + add/update grades
- `POST /students/<roll>/grades` – save grades
- `GET /reports/subject?subject=Math` – topper + class average, table
- `GET /health` – health check

## 5) Deployment (Heroku)

> You need a Heroku account and the Heroku CLI.

```bash
# from inside the project folder
heroku create student-performance-tracker-<yourname>
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a student-performance-tracker-<yourname>
git push heroku HEAD:main
# or: git push heroku master
heroku open
```

### Alternative: Render
1. Push this repo to GitHub.
2. Create a new **Web Service** on Render.
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `gunicorn app:app`
5. Choose a free instance; deploy.

## 6) Using the App

- **Add a student** from the home page.
- Click **Open** to view details and add grades.
- Go to **Subject Report** to see topper and class average.

## 7) Notes

- Default DB is SQLite (`students.db`). To use MySQL or Postgres, change the connection string in `create_db_app()` in `tracker.py`, e.g.:
  ```python
  create_db_app("mysql+pymysql://user:password@host/dbname")
  ```
  and install the relevant driver in `requirements.txt`.

- The CLI and the Web app share the same OOP layer, so they operate on the same database file.

## 8) Screenshots (optional)
Add screenshots/GIFs here once running locally or online.

---

Happy tracking!
