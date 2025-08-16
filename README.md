# Feedback App (Flask + SQLite)

Small Flask app with an SQLite database for collecting user feedback. Uses SQLAlchemy ORM and Bcrypt for password hashing.

## Setup & Run
```bash
pip install -r requirements.txt  # or: pip install Flask Flask_SQLAlchemy Flask_Bcrypt tabulate
python app.py
```
Open: http://127.0.0.1:5000

## Database
- `user`: id (PK), username (UNIQUE), password_hash  
- `feedback`: id (PK), username, message

## Admin
Admin page at `/admin`. Create a user named **admin** via Signup, then log in.

## Structure
```
app.py
instance/feedback.db
static/style.css
templates/{login,signup,feedback,admin}.html
view_db.py
```
