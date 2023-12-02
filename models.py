from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)
    
<<<<<<< HEAD
    # TODO put the table logic in the 
=======
# TODO put all the classes + methods in here (if we can)
>>>>>>> c2fe2b0a8e824b6ec9b29f70e5464660a13d93ea
