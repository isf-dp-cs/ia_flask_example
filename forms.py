from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class StudentForm(FlaskForm):
    name = StringField('Enter Name:',validators=[DataRequired()])
    science1 = SelectField('Select a Science', choices=[('None', 'None'),('CS', 'Computer Science'), ('BIO', 'Biology'), ('CHEM', 'Chemistry')])
    science2 = SelectField('Select a Science', choices=[('None', 'None'),('CS', 'Computer Science'), ('BIO', 'Biology'), ('CHEM', 'Chemistry')])
    science3 = SelectField('Select a Science', choices=[('None', 'None'),('CS', 'Computer Science'), ('BIO', 'Biology'), ('CHEM', 'Chemistry')])
    graduation_year = IntegerField('Enter Graduation Year',default=2027)
    submit = SubmitField('Submit')



class ReportForm(FlaskForm):
    num_groups = IntegerField('Enter Number of Groups:', default=2 ,validators=[DataRequired(),NumberRange(min=1, max=10)])
    graduation_year = IntegerField('Enter Graduation Year', default=2027)

    submit = SubmitField('Submit')
