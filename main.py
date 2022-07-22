# wk4/frontend-copy
# This is the main file.
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, RecipeSearchForm
from login import LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from py_edamam import Edamam
import os

app = Flask(__name__)  # this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app)  ## add this line
bcrypt = Bcrypt(app)  # code to create bcrypt wrapper for flask app
app.config["SECRET_KEY"] = "39e544a7b87e65b3d845915b1533104f"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
name = None


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    recipe_url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.username}') has saved Recipe('{self.recipe_url}')"


@app.route(
    "/", methods=["GET", "POST"]
)  # this tells you the URL the method below is related to
def home():
    search = RecipeSearchForm(request.form)
    if request.method == "POST":
        return search_results(search)

    e = Edamam(
        recipes_appid=os.environ.get("RECIPE_ID"),
        recipes_appkey=os.environ.get("RECIPE_KEY"),
    )

    # main_ingred_one = 'tofu'
    # main_ingred_two = 'pasta'
    # main_ingred_three = 'ice cream'
    # collection_one = e.search_recipe(main_ingred_one)['hits']
    # collection_two = e.search_recipe(main_ingred_two)['hits']
    # collection_three = e.search_recipe(main_ingred_three)['hits']

    # recipe_info = []
    # recipe_info2 = []
    # recipe_info3 = []
    # for i in range(2):
    #     recipe_info.append(collection_one[i]['recipe'])
    #     recipe_info2.append(collection_two[i]['recipe'])
    #     recipe_info3.append(collection_three[i]['recipe'])

    return render_template(
        "home.html",
        subtitle="Welcome to the Internet Cookbook",
        text="Browse the recipes or search for one",
    )  # this prints HTML to the webpage


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # checks if entries are valid
        if form.validate_on_submit():
            pw_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(
                username=form.username.data, email=form.email.data, password=pw_hash
            )
            db.session.add(user)
            db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))  # if so - send to home page
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login = LoginForm()
    if login.validate_on_submit():  # checks if entries are valid
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
                        flash(
                            "You have input the incorrect login information or password"
                        )
                    else:
                        flash("You have successfully logged in")
                        name = login_username

                        return redirect(url_for("user"))
                if query_email:
                    hash_pass = query_email.password
                    if not bcrypt.check_password_hash(hash_pass, login_pass):
                        flash(
                            "You have input the incorrect login information or password"
                        )
                    else:
                        flash("You have successfully logged in")
                        name = query_email.username
                        return redirect(url_for("user"))
            else:
                flash("You have input the incorrect login information or password")
    return render_template("signin.html", title="Log In", form=login)


@app.route("/user", methods=["GET", "POST"])
def user():
    subtitle = ""
    text = ""
    if name is None:
        subtitle = "Hello User"
        text = "You have not logged in to the user page"
    else:
        subtitle = f"Hello {name}"
        text = "You are logged in to the user page"

    search = RecipeSearchForm(request.form)
    if request.method == "POST":
        return search_results(search)

    return render_template("user_page.html", subtitle=subtitle, text=text, form=search)


@app.route("/results", methods=["POST"])
def search_results(search):
    result = request.form["recipe"]
    subtitle = f"Recipe results for {result}"

    e = Edamam(
        recipes_appid=os.environ.get("RECIPE_ID"),
        recipes_appkey=os.environ.get("RECIPE_KEY"),
    )

    main_ingred = result

    collection = e.search_recipe(main_ingred)["hits"]

    recipe_info = []
    for i in range(len(collection)):
        recipe_info.append(collection[i]["recipe"])

    return render_template("results.html", subtitle=subtitle, recipes=recipe_info)


@app.route("/save", methods=["POST"])
def save_to_database():

    saved_recipe = request.form["saveBtn"]

    if name is None:
        return redirect(url_for("login"))
    else:
        recipe = Recipe(username=name, recipe_url=saved_recipe)
        db.session.add(recipe)
        db.session.commit()
    user_recipes = Recipe.query.filter_by(username=name).all()
    return render_template("saved_recipes.html", data=user_recipes)


@app.route("/redirect", methods=["GET", "POST"])
def go_to_saved():
    if name is None:
        return redirect(url_for("login"))
    user_recipes = Recipe.query.filter_by(username=name).all()
    return render_template("saved_recipes.html", username=name, data=user_recipes)


if __name__ == "__main__":  # this should always be at the end
    app.run(debug=True, host="0.0.0.0")
