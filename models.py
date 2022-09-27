from datetime import datetime as dt
from app import db

#Beginning of Database Controls
#Creates user Table (class)
class User(db.Model):
    #Create tablename, may need to delete
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    track = db.relationship('Trackinsight', backref = 'author', lazy = True)
    def __repr__(self):
        return f"User('{self.email}')"
#Creates TrackInsight Class
class Trackinsight(db.Model):
    __tablename__ = "trackinsight"
    id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(120),db.ForeignKey('user.email'), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = dt.utcnow)
    track_content = db.Column(db.Text, nullable = False)

    #need defs

##END OF DATABASE CONTROLS