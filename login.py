from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

<<<<<<< HEAD

class LoginForm(FlaskForm):
    username = StringField("Username or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
=======
class LoginForm(FlaskForm):
    username = StringField('Username or Email',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
>>>>>>> 97996f02d99048718a55303ac733180478cd68d2
