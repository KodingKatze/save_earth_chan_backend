import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    default_database_path = "postgres://vxpvpxedsezapi:42a661d20ae59f880c133ffa92540d4b44587cbe7f57283b18ef2520e4e0185a@ec2-3-89-0-52.compute-1.amazonaws.com:5432/d1pkuq86o3csst"
    database_path = os.getenv('DATABASE_URL', default_database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Disaster(db.Model):
    __tablename__ = 'Disaster'

    id = db.Column(db.Integer, primary_key=True)
    EventTitle = db.Column(db.String(150), unique=False)
    Description = db.Column(db.String(255), unique=False)
    Location = db.Column(db.String(200), unique=False)
    Pictures = db.Column(db.LargeBinary)

    def toJson(self):
        return {
            'id': self.id,
            'eventTitle': self.EventTitle,
            'description': self.Description,
            'location': self.Location,
            'picture': self.Pictures or None
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()