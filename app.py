from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Patient

app = Flask(__name__)
app.secret_key = 'pdms_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pdms.sqlite'
db.init_app(app)

# ----------------- ROUTES ----------------------

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html', error="Invalid login credentials!")

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    patients = Patient.query.all()
    return render_template('dashboard.html', patients=patients)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        condition = request.form['condition']
        new_patient = Patient(full_name=name, age=age, gender=gender, condition=condition)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_patient.html')

@app.route('/view_patients')
def view_patients():
    if 'username' not in session:
        return redirect(url_for('login'))
    patients = Patient.query.all()
    return render_template('view_patients.html', patients=patients)

@app.route('/reports')
def reports():
    if 'username' not in session:
        return redirect(url_for('login'))
    patients = Patient.query.all()
    return render_template('reports.html', patients=patients)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
