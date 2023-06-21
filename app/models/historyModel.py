from app import db
from sqlalchemy.sql import func

from app.models.userModel import Users


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(Users.id_user))
    heart_rate = db.Column(db.String(200))
    status_heart_rate = db.Column(db.String(200))
    oxy_rate = db.Column(db.String(200))
    status_oxy_rate = db.Column(db.String(200))
    result = db.Column(db.String(200))
    category = db.Column(db.String(200))
    date = db.Column(db.Date)

    def __init__(self, id_user, heart_rate, status_heart_rate, oxy_rate, status_oxy_rate, result, category, date):
        self.id_user = id_user
        self.heart_rate = heart_rate
        self.status_heart_rate = status_heart_rate
        self.oxy_rate = oxy_rate
        self.status_oxy_rate = status_oxy_rate
        self.result = result
        self.category = category
        self.date = date