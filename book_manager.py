import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(os.path.dirname(__file__), 'bookdatabase.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development

db = SQLAlchemy(app)



    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(50))
    publisher = db.Column(db.String(50))
    publication_year = db.Column(db.Integer)
    copies_available = db.Column(db.Integer)
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
    # ... other fields related to an address

    def __repr__(self):
        return f"{self.street}, {self.city}, {self.state}"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    account_status = db.Column(db.String(20))

    def __repr__(self):
        return self.name


def create_tables():
    with app.app_context():
        db.create_all()
        # Create tables for Address, User, and other models if they're not already created
        db.session.commit()

        
@app.route("/updateBook", methods=["POST"])
def updateBook():
    book_id = request.form.get("book_id")
    new_title = request.form.get("new_title")  
    new_genre = request.form.get("new_genre")
    new_publisher = request.form.get("new_publisher")
    new_publication_year = request.form.get("new_publication_year")
    new_copies_available = request.form.get("new_copies_available")
    new_author_name = request.form.get("new_author_name")

    book = Book.query.get(book_id)
    if book:
        book.title = new_title
        book.genre = new_genre
        book.publisher = new_publisher 
        book.publication_year = new_publication_year
        book.copies_available = new_copies_available

        # Check if the author exists, if not, create a new one
        author = Author.query.filter_by(name=new_author_name).first()
        if not author:
            author = Author(name=new_author_name)
            db.session.add(author)

        book.author = author

        db.session.commit()

    return redirect("/")

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

    new_book = Book(title=title, genre=genre, publisher=publisher,
                    publication_year=publication_year, copies_available=copies_available, author=author)
    db.session.add(new_book)
    db.session.commit()

    return redirect("/")

@app.route("/addUser", methods=["POST"])
def add_user():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address_id = request.form.get("address_id")
    account_status = request.form.get("account_status")

    new_user = User(name=name, email=email, phone=phone, address_id=address_id, account_status=account_status)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route("/updateUserTable", methods=["POST"])
def update_user_table():
    user_id = request.form.get("user_id")
    new_name = request.form.get("new_name")
    new_email = request.form.get("new_email")
    new_phone = request.form.get("new_phone")
    new_address_id = request.form.get("new_address_id")
    new_account_status = request.form.get("new_account_status")

    

    user = User.query.get(user_id)
    if user:
        print("User found. Attempting update...")
        try:
            if new_name is not None:
                user.name = new_name
            if new_email is not None:
                user.email = new_email
            if new_phone is not None:
                user.phone = new_phone
            if new_address_id is not None:
                user.address_id = new_address_id
            if new_account_status is not None:
                user.account_status = new_account_status
            print(f"Received values: user_id={user_id}, new_name={new_name}, new_email={new_email}, ...")
            db.session.commit()
            print("User updated successfully!")
        except Exception as e:
            print(f"Error updating user: {e}")
    else:
        print("User not found!")

    return redirect("/")



@app.route("/deleteUser", methods=["POST"])
def delete_user():
    user_id = request.form.get("user_id")

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
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
    return render_template("home.html", books=books, users=users)


if __name__ == "__main__":
    create_tables()  # Create tables before running the app
    app.run(debug=True)
