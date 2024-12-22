import time
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import secrets
from movies import Movies



app = Flask(__name__)
class Base(DeclarativeBase):
    pass


#Initilize the flask  and the db objects
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///userfav"
db = SQLAlchemy(model_class= Base)
db.init_app(app)

#Creates the db for the user info if they want to login
class Users(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key= True, unique= True)
    name: Mapped[str] = mapped_column(String, nullable= False)
    email: Mapped[str] = mapped_column(String(50), unique= True, nullable= False)
    password: Mapped[int] = mapped_column(Integer, nullable= False)

    # Establish relationship with UserFav
    favorites = relationship("UserFav", back_populates="user", cascade="all, delete-orphan")

class UserFav(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key= True, unique= True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable= False)
    movie: Mapped[str] = mapped_column(String, nullable= False)
    image: Mapped[str] = mapped_column(String, nullable= False)
    release_date: Mapped[int] = mapped_column(Integer, nullable= False)
    rating: Mapped[int] = mapped_column(Integer, nullable= False)

    # Relationship back to Users
    user = relationship("Users", back_populates="favorites")




with app.app_context():
    db.create_all()





#Home page
@app.route("/")
def home():



    return render_template("index.html")


@app.route("/register", methods= ["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        result = db.session.execute(db.select(Users).where(Users.email == email)).scalar()
        user = result.email

        if user == email:
            flash("You already have an account registered")
            time.sleep(2)
            return redirect(url_for("login"))

        else:
            password = generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8)
            new_user = Users(name= name, email= email, password= password )
            db.session.add(new_user)
            db.session.commit()

            #Todo: add the login user verified later to make the user info load throughout the pages -----------------------------------
            return jsonify(success= f"Your account was created successfully. Hashed password: {password}")


    return render_template("register.html")




@app.route("/login", methods= ["POST", "GET"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #checks to see if the user is in the database
        result = db.session.execute(db.select(Users).where(Users.email == email))
        user = result.scalar()
        if not user:
            flash("Email don't exist. Create an account first")
            return render_template(url_for("register"))

        #TODO check the hashpassword with the inputted password
        # session["email"] = result.email
        # session["username"] = result.name

        return jsonify(success= "Successfully logged in")
        




    return "Get request"

#This route will generate 8 random movies from  a genre
@app.route("/random_movie", methods= ["GET", "POST", "DELETE"])
def random_movie():

    #If the user wants to add a favorite movie to their list
    if request.method == "POST":
        movie = request.form.get("movie")
        image = request.form.get("image")
        release_date = request.form.get("release_date")
        rating = request.form.get("rating")

        #Grab the user_id so the fav movie can be saved correctly
        email = request.form.get("email")
        result = db.session.execute(db.select(Users).where(Users.email == email)).scalar()


        #Todo uncomment when done testing the API's
        # user = session["username"]
        # email = session["email"]
        if result is not None:
            user = result.id
            new_fav_movie = UserFav(user_id= user, movie= movie, image= image, rating= rating, release_date= release_date)
            db.session.add(new_fav_movie)
            db.session.commit()


            #Todo when the html is ready change the return to somthing else -----------------------
            return jsonify(success= "The movie was added to your favorites")
        else:
            return jsonify(error= "User not found"), 404



    #Takes the movie the user favorite and
    elif request.method == "DELETE":
        movie = request.form.get("movie")

        # Grab the user_id so the fav movie can be saved correctly
        email = request.form.get("email")
        user_result = db.session.execute(db.select(Users).where(Users.email == email)).scalar()
        userfav_result = db.session.execute(db.select(UserFav).where(UserFav.id == user_result.id)).scalar()

        if userfav_result:
            result = db.session.execute(db.select(UserFav).where(UserFav.id == userfav_result.id)).scalar()
            delete_movie = result.movie
            print(delete_movie)
            # db.session.delete(deleted_movie)
            # db.session.commit()

            return jsonify(success= "Your movie was successfully deleted")
        else:
            return jsonify(error= "Movie dont exist in your favorites")

    #returns random movies by genre
    mov = Movies()
    movies = mov.random_movie_genre()
    movie = movies
    print("error")



    return render_template("random_movie.html", movie= movie)


@app.route("/search", methods= ["GET", "POST"])
def search_movie():
    title = request.args.get("query")

    mov = Movies()
    movie = mov.movie("search", title)

    return render_template("search.html", movie= movie)


























if __name__ == "__main__":
    app.run(debug= True)