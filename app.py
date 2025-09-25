from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MySQL config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/crm_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELS
class User(db.Model):
    __tablename__ = 'users'  # table name must match in MySQL
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default="PENDING")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ROUTES
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials","danger")
    return render_template('login.html', current_year=datetime.utcnow().year)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        user = User(username=username,email=email,password_hash=password,role=role)
        db.session.add(user)
        db.session.commit()
        flash("User registered! Login now.","success")
        return redirect(url_for('login'))
    return render_template('register.html', current_year=datetime.utcnow().year)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template(
        'dashboard.html',
        username=session.get('username'),
        role=session.get('role'),
        usernames=[u.username for u in users],
        tasks_per_user=[Task.query.filter_by(assigned_to=u.id).count() for u in users],
        completed_tasks_per_user=[Task.query.filter_by(assigned_to=u.id, status='COMPLETED').count() for u in users],
        current_year=datetime.utcnow().year
    )
@app.route('/admin/home')
def admin_home():
    users_count = User.query.count()
    tasks_count = Task.query.count()
    recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()
    return render_template('admin_home.html', users_count=users_count,
                           tasks_count=tasks_count, recent_tasks=recent_tasks)

@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password_hash = generate_password_hash(request.form['password'])
        role = request.form['role']
        user = User(username=username, email=email, password_hash=password_hash, role=role)
        db.session.add(user)
        db.session.commit()
        flash("User added successfully!", "success")
        return redirect(url_for('admin_home'))
    return render_template('add_user.html')

@app.route('/admin/activity_logs')
def admin_activity_logs():
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).all()
    return render_template('activity_logs.html', logs=logs)

@app.route('/admin/assign_task', methods=['GET', 'POST'])
def assign_task():
    users = User.query.all()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        assigned_to = request.form['assigned_to']
        task = Task(title=title, description=description, assigned_to=assigned_to)
        db.session.add(task)
        db.session.commit()
        flash("Task assigned successfully!", "success")
        return redirect(url_for('admin_home'))
    return render_template('assign_task.html', users=users)



@app.route('/users')
def users_page():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/tasks')
def tasks_page():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)
@app.route('/activity_logs')
def activity_logs_page():
    logs = ActivityLog.query.all()
    return render_template('activity_logs.html', logs=logs)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)
