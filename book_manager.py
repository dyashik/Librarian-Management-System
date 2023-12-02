import os
from sqlite3 import IntegrityError
import time
from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(os.path.dirname(__file__), 'bookdatabase.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development

#create database
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    genre = db.Column(db.String(50))
    publisher = db.Column(db.String(50))
    publication_year = db.Column(db.Integer)
    copies_available = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return self.title

# Define the Author and Book models
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return self.name
    
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"{self.street}, {self.city}, {self.state}"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=True)
    address = db.Column(db.String(200))
    zip_code = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)  # Update this line
    status = db.Column(db.String(20))

    def __repr__(self):
        return self.name


# DO NOT TOUCH
def create_tables():
    with app.app_context():
        db.create_all()
        # Create tables for Address, User, and other models if they're not already created
        db.session.commit()

# creates a book not actually updating a book
@app.route("/updateBook", methods=["POST"])
def updateBook():
    book_id = request.form.get("book_id")
    new_title = request.form.get("new_title")  
    new_genre = request.form.get("new_genre")
    new_publisher = request.form.get("new_publisher")
    new_publication_year = request.form.get("new_publication_year")
    new_copies_available = request.form.get("new_copies_available")
    new_author_name = request.form.get("new_author_name")



    # Check if the title exists for a book other than the current book being updated
    existing_book = Book.query.filter(Book.title == new_title, Book.id != request.form.get("book_id")).first()

    if existing_book:
        return redirect("/?status=error&message=Title already in use")  # Redirect with status and message in the URL

    # Continue with the update or insertion since the title is unique
    book_id = request.form.get("book_id")
    book = Book.query.get(book_id)
    if book:
        book.title = new_title
        book.genre = new_genre
        book.publisher = new_publisher
        book.publication_year = new_publication_year
        book.copies_available = new_copies_available
        
        author = Author.query.filter_by(name=new_author_name).first()
        
        if not author:
            author = Author(name=new_author_name)
            db.session.add(author)
        
        book.author = author

        db.session.commit()

    return redirect("/?status=success&message=Book updated successfully")
@app.route("/updateBookTable", methods=["POST"])
def update_book_table():
    title = request.form.get("title")
    genre = request.form.get("genre")
    publisher = request.form.get("publisher")
    publication_year = request.form.get("publication_year")
    copies_available = request.form.get("copies_available")
    author_name = request.form.get("author_name")

    author = Author.query.filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        db.session.add(author)
        
    
    existing_book = Book.query.filter_by(title=title).first()
    
    print(existing_book)
    
    if existing_book:
        return redirect("/?status=error&message=Title already in use")  # Redirect with status and message in the URL

    new_book = Book(title=title, genre=genre, publisher=publisher,
                    publication_year=publication_year, copies_available=copies_available, author=author)
    
    db.session.add(new_book)
    db.session.commit()

    return redirect("/?status=success&message=User added Sucessfully")

@app.route("/addUser", methods=["POST"])
def add_user():
    user_id = request.form.get("user_id")
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    zip_code = request.form.get("zip_code")
    address = request.form.get("address")
    status = request.form.get("status")

    existing_user_email = User.query.get(email)
    existing_user_phone = User.query.get(phone)
    
    if existing_user_email or existing_user_phone:
        return redirect("/?status=error&message=Email / Phone Number already in use")  # Redirect with status and message in the URL
    else :
        new_user = User(id=user_id, name=name, email=email, phone=phone, address=address, zip_code=zip_code, status=status)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/?status=success&message=User added Sucessfully")  # Redirect with status and message in the URL
        

    return redirect("/")

@app.route("/updateUserTable", methods=["POST"])
def update_user_table():
    user_id = request.form.get("user_id")
    new_name = request.form.get("new_name")
    new_email = request.form.get("new_email")
    new_phone = request.form.get("new_phone_number")
    new_address = request.form.get("new_address")
    new_zip = request.form.get("new_zip_code")
    new_status = request.form.get("new_status")

    user_email = User.query.get(new_email)
    user_phone = User.query.get(new_phone)
    user = User.query.get(user_id)
    
    if user_email is not user or user_phone is not user:
        return redirect("/?status=error&message=Email / Phone Number already in use")  # Redirect with status and message in the URL
    else :
        user.name = new_name
        user.email = new_email
        user.phone = new_phone
        user.address = new_address
        user.zip_code = new_zip
        user.status = new_status
        db.session.commit()
        return redirect("/?status=success&message=User was successfully added!.")  # Redirect with status and message in the URL



@app.route("/deleteUser", methods=["POST"])
def delete_user():
    user_id = request.form.get("user_id")

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect("/")


#Author stuff
@app.route("/addAuthor", methods=["POST"])
def add_author():
    author_id = request.form.get("author_id")
    author_name = request.form.get("author_name")

    # Check if the author id already exists
    existing_author_id = Author.query.get(author_id)
    if existing_author_id:
        return redirect("/?status=error&message=Author ID already in use")  # Redirect with status and message in the URL

    # Check if the author name already exists
    existing_author_name = Author.query.filter_by(name=author_name).first()
    if existing_author_name:
        return redirect("/?status=error&message=Author name already in use")  # Redirect with status and message in the URL

    # Continue with the addition since the author id and name are unique
    new_author = Author(id=author_id, name=author_name)
    db.session.add(new_author)
    db.session.commit()

    return redirect("/?status=success&message=Author added Successfully")



@app.route("/updateAuthorTable", methods=["POST"])
def update_author_table():
    author_id = request.form.get("author_id")
    new_author_name = request.form.get("new_author_name")

    author = Author.query.get(author_id)
    if author:
        existing_author = Author.query.filter(Author.name == new_author_name, Author.id != author_id).first()

        if existing_author:
            return redirect("/?status=error&message=Author name already in use")  # Redirect with status and message in the URL

        author.name = new_author_name
        db.session.commit()

    return redirect("/?status=success&message=Author updated successfully")


@app.route("/deleteAuthor", methods=["POST"])
def delete_author():
    author_id = request.form.get("author_id")

    author = Author.query.get(author_id)
    if author:
        db.session.delete(author)
        db.session.commit()

    return redirect("/")


# Delete route
@app.route("/delete", methods=["POST"])
def delete():
    book_id = request.form.get("book_id")
    # Retrieve the book from the database using the book_id
    book = Book.query.get(book_id)
    if book:
        # If the book exists, delete it from the database
        db.session.delete(book)
        db.session.commit()
    return redirect("/")





@app.route("/", methods=["GET", "POST"])
def home():
    books = Book.query.all()
    users = User.query.all()  # Fetch all
    authors = Author.query.all()
    return render_template("home.html", books=books, users=users, authors=authors)


if __name__ == "__main__":
    create_tables()  # Create tables before running the app
    app.run(debug=True)
