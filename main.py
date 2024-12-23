import time
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import secrets
from movies import Movies



class Base(DeclarativeBase):
    pass

app = Flask(__name__)
#Gives flask a secret key
app.secret_key = secrets.token_urlsafe(24)

#Initilize the flask  and the db objects
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///userfav"
db = SQLAlchemy(model_class= Base)
db.init_app(app)

#Gives flask a secret key
app.secret_key = secrets.token_urlsafe(24)



#Login initialize
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" #Redirect users to the login page if the route is protected

#returns all the user data buy using the PK
@login_manager.user_loader
def login_user(user_id):
    return db.session.get(Users, user_id)





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
    if current_user.is_authenticated:
        print(current_user.username)

    return render_template(
        "index.html",
        user=current_user.is_authenticated,
        username=current_user.username if current_user.is_authenticated else None
    )



@app.route("/register", methods= ["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        result = db.session.execute(db.select(Users).where(Users.email == email)).scalar()

        if result is not None and result.email == email:
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

        # Check if the user is in the database
        result = db.session.execute(db.select(Users).where(Users.email == email))
        user = result.scalar()

        if user and check_password_hash(user.password, password):
            # Log the user in
            login_user(user.id)
            # Redirect to the homepage after login
            flash("You have successfully logged in!")
            time.sleep(1)
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.")
            return redirect(url_for("login"))

            # flash("Email don't exist. Create an account first")
                # return render_template(url_for("register"))
    else:

        return render_template("login.html")




@app.route("/logout", methods= ["GET", "POST"])
def logout():

    if request.method == "POST":
        logout_user()
        return jsonify(logout= "You have been logged out")
        # return redirect(url_for("login"))

    return jsonify(loaded= "loaded logout page")
        




#This route will generate 8 random movies from  a genre
@app.route("/random_movie", methods= ["GET", "POST", "DELETE"])
def random_movie():

    if current_user.is_authenticated:
        #If the user wants to add a favorite movie to their list
        if request.method == "POST":
            movie = request.form.get("movie")
            image = request.form.get("image")
            release_date = request.form.get("release_date")
            rating = request.form.get("rating")

            result = db.session.execute(db.select(UserFav).where(UserFav == current_user.id)).scalars()

            if result is not None and movie not in result.movie:
                new_fav_movie = UserFav(user_id= current_user.id, movie= movie, image= image, rating= rating, release_date= release_date)
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
            user_result = current_user.id
            userfav_result = db.session.execute(db.select(UserFav).where(UserFav.id == user_result)).scalar()

            if userfav_result:
                delete_movie = userfav_result.movie
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



@app.route("/dashboard", methods= ["GET"])
@login_required
def dashboard():

    return jsonify(success= f"Hello: {current_user.name}. Your Id is {current_user.id}")


















if __name__ == "__main__":  #Checkt to see if the program is running locally
    app.run(debug= True)