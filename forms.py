from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerRangeField, StringField,PasswordField, SelectField, IntegerField, TextAreaField, DecimalField, FileField, SearchField, EmailField, RadioField, DateField,ValidationError
from wtforms.validators import InputRequired, NumberRange,EqualTo, DataRequired,Length, Optional
import datetime

def not_in_past(form, field):
    if field.data < datetime.date.today():
        raise ValidationError("Date cannot be in the past.")

def validate_progress(self, field):
    if self.Goal.data is not None and field.data is not None:
        if field.data > self.Goal.data:
            raise ValidationError("Progress cannot be greater than the goal.")

def no_only_spaces(form, field):
    if not field.data or not field.data.strip():
        raise ValidationError("This field cannot be empty or just spaces.")


class searchForm(FlaskForm):
    search = StringField('Search Products')
    submit = SubmitField('submit')

class LogForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),no_only_spaces])
    password1 = PasswordField('Please create a password', validators=[InputRequired()])
    password2 = PasswordField('Please Re-enter the password', validators=[InputRequired(),EqualTo("password1",'The passwords must be equal')])
    submit = SubmitField('Submit')
    
class cartAdd(FlaskForm):
    select = SelectField('Quantity', coerce=int)
    type = RadioField('Type', choices=['Physical','Digital'])
    submit = SubmitField('Add To Cart')

class commentForm(FlaskForm):
    comment = TextAreaField('Product Description',validators=[ Length(max=250)])
    submit = SubmitField('confirm')

class updateForm(FlaskForm):
    changeName = StringField('Product Name', validators=[InputRequired(), DataRequired()])
    changeStock = IntegerField('Stock Remaining', validators=[InputRequired(),NumberRange(min =1)])
    changePrice = DecimalField('Product Price', places=2, validators=[DataRequired(),NumberRange(min =1,max = 3000)])
    changeDesc = TextAreaField('Product Description',validators=[ Length(max=650)])
    submit = SubmitField('confirm')


class newBudget(FlaskForm):
    Name = StringField('What are you saving up towards?', validators=[InputRequired(), no_only_spaces])
    Progress = IntegerField('How much have you invested so far?', validators=[InputRequired(), NumberRange(min =0),validate_progress])
    Goal = IntegerField('How much do you need to save?', validators=[InputRequired(), NumberRange(min =1)])
    Deadline = DateField('When is the due date?', format='%Y-%m-%d', validators=[InputRequired(),not_in_past])
    submit = SubmitField('confirm')



class updateBudget(FlaskForm):
    progressAdvance = IntegerField('How much more are you investing?', validators=[ NumberRange(min =0), Optional()])
    progressWithdraw = IntegerField('How much are you withdrawing?', validators=[ NumberRange(min =0), Optional()])
    submit = SubmitField('confirm')
    

class newUsername(FlaskForm):
    username = StringField('Current Username', validators=[InputRequired(), no_only_spaces])
    password = PasswordField('password', validators=[InputRequired()])
    newUser = StringField('New Username', validators=[InputRequired()])
    submit = SubmitField('submit')

class newPass(FlaskForm):
    password1 = PasswordField('Please enter previous password', validators=[InputRequired()])
    password2 = PasswordField('Please enter a new password', validators=[InputRequired()])
    password3 = PasswordField('Please re-enter the new password', validators=[InputRequired(),EqualTo("password2",'The passwords must be equal')])
    submit = SubmitField('submit')

class newPic(FlaskForm):
    image = FileField('Product Image',validators=[DataRequired()])
    submit = SubmitField('confirm')

class filterForm(FlaskForm):
    searchFilter = SearchField('Search Products: ')
    filterPrice = IntegerRangeField('Filter Price: ', validators=[ NumberRange(min=1, max=3000)])
    search = SubmitField('search')

class friendForm(FlaskForm):
    searchFilter = SearchField('Search Users: ',validators=[InputRequired()])
    search = SubmitField('search')

class newsForm(FlaskForm):
    email = EmailField('Your Email', validators=[InputRequired()])
    subscribe = SubmitField('Subscribe')