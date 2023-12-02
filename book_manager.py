import datetime
import os
from sqlite3 import IntegrityError
import time
from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import *

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
    address = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"{self.address}, {self.zip_code}"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(10))
    address = db.Column(db.String(200))
    zip_code = db.Column(db.Integer, nullable=False)  # Update this line
    status = db.Column(db.String(20))
    
    def __repr__(self):
        return self.name
    

class Loan(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    book_title = db.Column(db.String(80), db.ForeignKey('book.title'), nullable=False)
    checkout_date = db.Column(db.String, nullable=False)
    due_date = db.Column(db.String, nullable=False)

    # user = db.relationship('User', backref=db.backref('loans', lazy=True))
    # book = db.relationship('Book', backref=db.backref('loans', lazy=True))

    def __repr__(self):
        return str(self.loan_id)

    
# DO NOT TOUCH
def create_tables():
    with app.app_context():
        db.create_all()
        # Create tables for Address, User, and other models if they're not already created
        db.session.commit()

# updating a book
@app.route("/updateBook", methods=["POST"])
def update_book():
    book_id = request.form.get("book_id")
    new_title = request.form.get("new_title")  
    new_genre = request.form.get("new_genre")
    new_publisher = request.form.get("new_publisher")
    new_publication_year = request.form.get("new_publication_year")
    new_copies_available = request.form.get("new_copies_available")
    new_author_name = request.form.get("new_author_name")

    # Check if the title exists for a book other than the current book being updated
    existing_book = Book.query.filter(Book.title == new_title, Book.id != book_id).first()

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
def create_book():
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

    return redirect("/?status=success&message=Book added Sucessfully")

@app.route("/addLoan", methods=["POST"])
def add_loan():
    loan_id = request.form.get("loan_id")
    user_email = request.form.get("user_email")

    book_title = request.form.get("book_title")
    checkout_date = request.form.get("checkout_date")
    due_date = request.form.get("due_date")

    # Check if the user with the given email or phone exists
    user = User.query.filter_by(email=user_email).first()
    print(user)
    if not user:
        return redirect("/?status=error&message=User not found")  # Redirect with status and message

    # Check if the book with the given title exists
    book = Book.query.filter(Book.title==book_title).first()
    if not book:
        return redirect("/?status=error&message=Book not found")  # Redirect with status and message

    updated_copies = book.copies_available - 1
    if updated_copies >= 0:
        db.session.execute(update(Book).where(Book.title == book_title).values(copies_available=updated_copies))
        db.session.commit()
    else:
        return redirect("/?status=error&message=Not Enough Copies") 
    
    try:
        # Check the format of the input date strings
        check_in_date = datetime.strptime(checkout_date, "%m/%d/%Y")
        return_date = datetime.strptime(due_date, "%m/%d/%Y")
    except ValueError:
        return redirect("/?status=error&message=Invalid Date Format") 

    # Compare the dates
    if check_in_date > return_date:
        return redirect("/?status=error&message=Check In after Due Date") 
    elif check_in_date == return_date:
        return redirect("/?status=error&message=Check In same day as Due Date") 
    
    # Continue with adding the loan if everything is valid
    new_loan = Loan(
        loan_id=loan_id,
        user_email=user_email,
        book_title=book_title,
        checkout_date=checkout_date,
        due_date=due_date
    )

    db.session.add(new_loan)
    db.session.commit()

    return redirect("/?status=success&message=Loan added successfully")


@app.route("/updateLoanTable", methods=["POST"])
def update_loan():
    loan_id = request.form.get("loan_id")
    new_checkout_date = request.form.get("new_checkout_date")
    new_due_date = request.form.get("new_due_date")
    
    try:
        # Check the format of the input date strings
        check_in_date = datetime.strptime(new_checkout_date, "%m/%d/%Y")
        return_date = datetime.strptime(new_due_date, "%m/%d/%Y")
    except ValueError:
        return redirect("/?status=error&message=Invalid Date Format") 

    # Compare the dates
    if check_in_date > return_date:
        return redirect("/?status=error&message=Check In after Due Date") 
    elif check_in_date == return_date:
        return redirect("/?status=error&message=Check In same day as Due Date") 
    print(loan_id)
    loan = Loan.query.get(loan_id)
    
    if loan:
        # Update the checkout_date and due_date
        loan.checkout_date = new_checkout_date
        loan.due_date = new_due_date
        print(loan.due_date)
        # Commit the changes
        db.session.commit()
        return redirect("/?status=success&message=Loan updated successfully")
    else:
        return redirect("/?status=error&message=Loan not found")

@app.route("/deleteLoan", methods=["POST"])
def delete_loan():
    loan_id = request.form.get("loan_id")
    print(loan_id)
    loan = Loan.query.filter_by(loan_id=loan_id).first()
    print(loan)
    if loan:
        book = Book.query.filter_by(title=loan.book_title).first()

        if book:
            # Update available copies in the Book table
            if book:
                # Update available copies in the Book table
                updated_copies = book.copies_available + 1
                book.copies_available = updated_copies  # Update the copies_available field in the Book model
                db.session.commit()

            # Delete the loan record
            db.session.delete(loan)
            db.session.commit()

    return redirect("/loans.html")

@app.route("/addUser", methods=["POST"])
def add_user():
    user_id = request.form.get("user_id")
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    zip_code = request.form.get("zip_code")
    address = request.form.get("address")
    status = request.form.get("status")

    existing_user_email = User.query.filter_by(email=email).first()
    existing_user_phone = User.query.filter_by(phone=phone).first()
    
    if existing_user_email or existing_user_phone:
        return redirect("/?status=error&message=Email / Phone Number already in use")  # Redirect with status and message in the URL
    else :
        
        existing_user_address = User.query.filter_by(address=address, zip_code=zip_code).first()
        
        if not existing_user_address:
            new_address = Address(address=address, zip_code=zip_code)
            db.session.add(new_address)
            db.session.commit()
        
        new_user = User(id=user_id, name=name, email=email, phone=phone, address=address, zip_code=zip_code, status=status)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/?status=success&message=User added Sucessfully")  # Redirect with status and message in the URL

@app.route("/updateUserTable", methods=["POST"])
def update_user_table():
    user_id = request.form.get("user_id")
    new_name = request.form.get("new_name")
    new_email = request.form.get("new_email")
    new_phone = request.form.get("new_phone_number")
    new_address = request.form.get("new_address")
    new_zip = request.form.get("new_zip_code")
    new_status = request.form.get("new_status")

    user = User.query.filter_by(id=user_id).first()
    user_email = User.query.filter_by(email=new_email).first()
    user_phone = User.query.filter_by(phone=new_phone).first()
    
    if user_email and user_email != user:
        return redirect("/?status=error&message=Email already in use")
    elif user_phone and user_phone != user:
        return redirect("/?status=error&message=Phone number already in use")
    else:
        user.name = new_name
        user.email = new_email
        user.phone = new_phone
        user.address = new_address
        user.zip_code = new_zip
        user.status = new_status
        db.session.commit()
        return redirect("/?status=success&message=User was successfully updated!")

@app.route("/addAddress", methods=["POST"])
def add_address():
    id = request.form.get("address_id")
    address = request.form.get("address")
    zip_code = request.form.get("zip_code")

    existing_address = Address.query.filter_by(address=address).first()
    
    if existing_address:
        return redirect("/?status=error&message=Address already in use")  # Redirect with status and message in the URL
    else :
        new_addy = Address(id=id, address=address, zip_code=zip_code)
        db.session.add(new_addy)
        db.session.commit()
        return redirect("/?status=success&message=User was successfully added!.")


@app.route("/deleteUser", methods=["POST"])
def delete_user():
    user_id = request.form.get("user_id")

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect("/users.html")


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

@app.route("/deleteAddress", methods=["POST"])
def delete_address():
    address_id = request.form.get("address_id")

    address = Address.query.get(address_id)
    if address:
        db.session.delete(address)
        db.session.commit()

    return redirect("/")

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
    loans = Loan.query.all()
    addresses = Address.query.all()
    return render_template("home.html", books=books, users=users, authors=authors, loans=loans, addresses=addresses)

@app.route("/books", methods=["GET", "POST"])
def book_page():
    home()
    books = Book.query.all()
    return render_template("books.html", books=books)

@app.route("/users", methods=["GET", "POST"])
def user_page():
    home()
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/authors", methods=["GET", "POST"])
def authors_page():
    home()
    authors = Author.query.all()
    return render_template("authors.html", authors=authors)

@app.route("/address", methods=["GET", "POST"])
def addresses_page():
    home()
    adderesses = Address.query.all()
    return render_template("addresses.html", adderesses=adderesses)

@app.route("/loans", methods=["GET", "POST"])
def loan_page():
    home()
    loans = Loan.query.all()
    return render_template("loans.html", loans=loans)

if __name__ == "__main__":
    create_tables()  # Create tables before running the app
    app.run(debug=True)
