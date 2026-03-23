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
           
            new_student = Student(name=data['name'], science=data['science'], graduation_year=data['graduation_year'])
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
    print(students)

    optimized_groups_list = assign_to_groups(students, num_groups)

    print(optimized_groups_list)

    # Convert to dictionary for Template and update DB
    groups = {}
    group_metrics = {} # Stores {Group_ID: Score}


    for idx, group_list in enumerate(optimized_groups_list):
        group_id = idx + 1
        groups[group_id] = group_list

        group_metrics[group_id] = diversity_score(group_list)
        print(diversity_score(group_list))

        for student in group_list:
            student.group = group_id
    
    db.session.commit()

    print(groups)
    print(group_metrics)

    return render_template(
            'report.html', 
            groups = groups,
            metrics=group_metrics,
           )

if __name__ == '__main__': 
    app.run(debug=True, port=5000)

    
