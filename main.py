from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import secrets
from movies import Movies



app = Flask(__name__)
class Base(DeclarativeBase):
    pass


#Initilize the flask  and the db objects
app.config["SQLALCHEMY_DATABASE_UI"] = "sqlite://users"
db = SQLAlchemy(model_class= Base)
db.init_app(app)

#Creates the db for the user info if they want to login
class Users(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key= True, unique= True)
    name: Mapped[str] = mapped_column(String, nullable= False)
    email: Mapped[str] = mapped_column(String(50), unique= True, nullable= False)
    password: Mapped[int] = mapped_column(Integer, nullable= False)



with app.app_context():
    db.create_all()







#Home page
@app.route("/")
def home():



    return render_template("index.html")


#This route will generate 8 random movies from  a genre
@app.route("/random_movie", methods= ["GET"])
def random_movie():

    mov = Movies()
    movies = mov.random_movie_genre()
    movie = movies
    print(movie)



    return render_template("random_movie.html", movie= movie)


@app.route("/search", methods= ["GET", "POST"])
def search_movie():
    title = request.args.get("query")

    mov = Movies()
    movie = mov.movie("search", title)
    print(movie)

    return render_template("search.html", movie= movie)


























if __name__ == "__main__":
    app.run(debug= True)