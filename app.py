from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ---------- MODELS ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    message = db.Column(db.Text, nullable=False)

# ---------- ROUTES ----------

@app.route('/')
def home():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if User.query.filter_by(username=username).first():
            return "Username already exists"

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = User.query.filter_by(username=username).first()

        # Debugging (optional)
        print("Username:", username)
        print("Password:", password)
        if user:
            print("Stored Hash:", user.password)

        # Check password
        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = user.username
            return redirect('/admin' if user.username == 'admin' else '/feedback')

        return "Invalid credentials"

    return render_template('login.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        fb = Feedback(username=session['user'], message=request.form['message'])
        db.session.add(fb)
        db.session.commit()
        return "Feedback submitted!"
    return render_template('feedback.html', username=session['user'])

@app.route('/admin')
def admin():
    if 'user' not in session or session['user'] != 'admin':
        return "Access denied"
    feedbacks = Feedback.query.all()
    return render_template('admin.html', feedbacks=feedbacks)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/delete_feedback')
def delete_feedback():
    if 'user' not in session or session['user'] != 'admin':
        return "Access denied"
    Feedback.query.delete()
    db.session.commit()
    return redirect('/admin')


# ---------- RUN ----------
if __name__ == '__main__':
    # Ensure DB exists
    with app.app_context():
        db.create_all()
    app.run(debug=True)
