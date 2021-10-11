import os
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.dialects import postgresql
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    default_database_path = "postgres://klysesgvmaxltp:acb6e9cf080fe74b322ec5c2f041e168356dd1c804e08b7566780dff014069a2@ec2-44-199-26-122.compute-1.amazonaws.com:5432/dedmcbhl0t8v6q"
    database_path = os.getenv('DATABASE_URL', default_database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class QueryType(str):
    def __str__(self) -> str:
        return self.lower()

class Disaster(db.Model):
    __tablename__ = 'Disaster'

    id = db.Column(db.Integer, primary_key=True)
    EventTitle = db.Column(db.String(150), unique=False)
    Description = db.Column(db.String(255), unique=False)
    Location = db.Column(db.String(200), unique=False)
    Pictures = db.Column(db.ARRAY(String), unique=False)
    Latitude = db.Column(db.FLOAT(), unique=False)
    Longitude = db.Column(db.FLOAT(), unique=False)
    Category = db.Column(postgresql.ARRAY(String), unique=False)

    def toJson(self):
        return {
            'id': self.id,
            'eventTitle': self.EventTitle,
            'description': self.Description,
            'location': self.Location,
            'picture': self.Pictures or None,
            'latitude': str(self.Latitude),
            'longtitude': str(self.Longitude),
            "categories": self.Category
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()