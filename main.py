# This is the main file.
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from login import LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app)  ## add this line
bcrypt = Bcrypt(app)             # code to create bcrypt wrapper for flask app
app.config['SECRET_KEY'] = '39e544a7b87e65b3d845915b1533104f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
name = None

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

@app.route("/")                          # this tells you the URL the method below is related to
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')      # this prints HTML to the webpage

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        if form.validate_on_submit():
            pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=pw_hash)
            db.session.add(user)
            db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)
@app.route("/login", methods=['GET', 'POST'])
def login():
    login = LoginForm()
    if login.validate_on_submit(): # checks if entries are valid
        if login.validate_on_submit():
            login_username = login.username.data
            login_pass = login.password.data
            query_username = User.query.filter_by(username=login_username).first()
            query_email = User.query.filter_by(email=login_username).first()
            if query_username or query_email:
                global name
                if query_username:
                    hash_pass = query_username.password
                    if not bcrypt.check_password_hash(hash_pass, login_pass):
                        flash('You have input the incorrect login information or password')
                    else:
                        flash('You have successfully logged in')
                        name = login_username
                        
                        return redirect(url_for('user'))
                if query_email:
                    hash_pass = query_email.password
                    if not bcrypt.check_password_hash(hash_pass, login_pass):
                        flash('You have input the incorrect login information or password')
                    else:
                        flash('You have successfully logged in')
                        name = query_email.username
                        return redirect(url_for('user'))
            else:
                flash('You have input the incorrect login information or password')
    return render_template('signin.html', title='Log In', form=login)
@app.route("/user")
def user():
    subtitle = ''
    text = ''
    if name is None:
        subtitle = 'Hello User'
        text = 'You have not logged in to the user page'
    else:
        subtitle = f'Hello {name}'
        text = 'You are logged in to the user page'
    return render_template('user_page.html', subtitle=subtitle, text=text )
if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")