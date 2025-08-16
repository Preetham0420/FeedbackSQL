\# Feedback App (Flask + SQLite)



A small feedback-capture web app built with \*\*Flask\*\*, \*\*SQLite\*\*, and \*\*SQLAlchemy\*\*.  

Supports signup/login (bcrypt-hashed), submitting feedback, and an admin view to review/clear entries.



\## How to Run

Run the app with:

python app.py



DB file: `instance/feedback.db` (auto-created/used).  

CLI viewer: `python view\_db.py`.



\## Tables

\- user(id PK, username UNIQUE, password\_hash)

\- feedback(id PK, username, message)



