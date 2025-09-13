from flask import Flask, render_template, request, redirect, session
from models import db, User, Performance, Syllabus
from study_planner import generate_study_plan
from questions_generator import generate_questions

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # if 'user_id' not in session:
    #     return redirect('/login')
    syllabus = Syllabus.query.all()
    return render_template('dashboard.html', syllabus=syllabus)

@app.route('/study_plan')
def study_plan():
    # if 'user_id' not in session:
    #     return redirect('/login')
    user_id = session['user_id']
    plan = generate_study_plan(user_id)
    return render_template('study_plan.html', plan=plan)

@app.route('/practice/<topic>')
def practice(topic):
    questions = generate_questions(topic)
    return render_template('practice.html', topic=topic, questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
