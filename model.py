from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class User(db.Model):
    __tablename__ = 'user'
 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    date = db.Column(db.DateTime,server_default=db.func.now())
 
    def __init__(self,name,email):
        self.name = name
        self.email = email
 
    def __repr__(self):
        return f"{self.name}:{self.email}"

class Height(db.Model):
    __tablename__ = 'height'
 
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer)
    height = db.Column(db.Float)
    date = db.Column(db.DateTime,server_default=db.func.now())
 
    def __init__(self,user,height):
        self.user = user
        self.height = height
 
    def __repr__(self):
        return f"{self.user}:{self.height}:{self.date}"


