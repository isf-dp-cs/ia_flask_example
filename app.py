# to run the server: 
# # flask --app app.py --debug run

from flask import Flask, request, render_template, url_for, redirect, session, flash, get_flashed_messages
from models import db, Student  # Import from your other file
import secrets
from forms import StudentForm, ReportForm
from random import shuffle
from helpers import *

app = Flask(__name__, static_url_path=f'/')
app.secret_key = secrets.token_hex(32)  # Required for CSRF protection
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"

# Link the db to this specific app
db.init_app(app)

# Create the tables if it does not exisit, ignore if it exists 
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/all", methods=['GET'])
def all():
    # Querying the database
    students = Student.query.all()
    return render_template(
            'all_students.html', 
            students = students,
           )


@app.route(f"/add", methods=['GET', 'POST'])
def form_add():
    form = StudentForm()

    if request.method == 'POST':
        if form.validate_on_submit(): 
            data = form.data       
           
            new_student = Student(
                name=data['name'], 
                science1=data['science1'], 
                science2=data['science2'], 
                science3=data['science3'], 
                graduation_year=data['graduation_year'])
            
            db.session.add(new_student)
            db.session.commit()

            return redirect(url_for('index'))


    return render_template(
            'form_add.html', 
            form = form)

@app.route(f"/report_config", methods=['GET', 'POST'])
def form_report():
    form = ReportForm()

    if request.method == 'POST':
        if form.validate_on_submit(): 
            data = form.data       
            print(data['num_groups'])
            return redirect(url_for('report', num_groups = data['num_groups']))

    return render_template(
            'form_report.html', 
            form = form)


@app.route("/report/<int:num_groups>", methods=['GET'])
def report(num_groups):
    # Querying the database
    students = Student.query.all()

    optimized_groups_list = assign_to_groups(students, num_groups)


    group_metrics = {} # Stores {Group_ID: Score}

    for i in range(len(optimized_groups_list)):
        group = optimized_groups_list[i]
        group_metrics[i] = diversity_score(group)

        for student in group:
            student.group_num = i
    
    db.session.commit()

    
    return render_template(
            'report.html', 
            metrics=group_metrics,
            optimized_groups_list=optimized_groups_list
           )

if __name__ == '__main__': 
    app.run(debug=True, port=5000)

    
