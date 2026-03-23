from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    name = StringField('Enter Name:',validators=[DataRequired()])
    science = SelectField('Select a Science', choices=[('CS', 'Computer Science'), ('BIO', 'Biology'), ('CHEM', 'Chemistry')])
    graduation_year = IntegerField('Enter Graduation Year',default=2027)

    submit = SubmitField('Submit')



class ReportForm(FlaskForm):
    num_groups = IntegerField('Enter Number of Groups:', default=2 ,validators=[DataRequired()])
    graduation_year = IntegerField('Enter Graduation Year', default=2027)

    submit = SubmitField('Submit')
