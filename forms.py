from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

<<<<<<< HEAD

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class RecipeSearchForm(FlaskForm):
    options = [
        ("All", "All"),
        ("Breakfast", "Breakfast"),
        ("Lunch", "Lunch"),
        ("Dinner", "Dinner"),
    ]
    select = SelectField(
        "Search for a recipe or input a main ingredient:", choices=options
    )
    search = StringField("")
=======
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class RecipeSearchForm(FlaskForm):
    options = [('All', 'All'),
               ('Breakfast', 'Breakfast'), 
               ('Lunch', 'Lunch'),
               ('Dinner', 'Dinner')]
    select = SelectField('Search for a recipe or input a main ingredient:', choices=options)
    search = StringField('')
>>>>>>> 97996f02d99048718a55303ac733180478cd68d2
