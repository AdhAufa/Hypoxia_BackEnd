from app import app
from flask import request, jsonify
from flask_marshmallow import Marshmallow
from app.models.userModel import Users
from app.models.historyModel import db, History
from datetime import date, datetime
from sqlalchemy import desc


ma = Marshmallow(app)

class HistorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_user', 'heart_rate', 'status_heart_rate', 'oxy_rate', 'status_oxy_rate', 'result', 'category', 'date')


HistorysSchema = HistorySchema()
HistoriesSchema = HistorySchema(many=True)

def postHistory(decodeToken):
    data = request.get_json()
    id_user = decodeToken.get('id_user')
    heart_rate = data['heart_rate']
    status_heart_rate = data['status_heart_rate']
    oxy_rate = data['oxy_rate']
    status_oxy_rate = data['status_oxy_rate']
    result = data['result']
    category = data['category']
    tanggal = date.today()

    newHistory = History(id_user, heart_rate, status_heart_rate, oxy_rate,status_oxy_rate,result, category,  tanggal)
    db.session.add(newHistory)
    db.session.commit()
    new = HistorysSchema.dump(newHistory)
    return jsonify({"msg": "Success add History", "status": 200, "data": new})

def getAllHistory(decodeToken):
    id_user = decodeToken.get('id_user')
    HistorysQuery = History.query.with_entities(History.id, History.id_user, History.heart_rate, History.status_heart_rate, History.oxy_rate,History.status_oxy_rate, History.category, History.result, History.date).filter(History.id_user == id_user).order_by(desc(History.date))
    Historys = HistoriesSchema.dump(HistorysQuery)
    return jsonify({"msg": "Success get History by id", "status": 200, "data": Historys})

def deleteHistory(id):
    history = History.query.get(id)
    db.session.delete(history)
    db.session.commit()
    HistoryDelete = HistorysSchema.dump(history)
    return jsonify({"msg": "Success Delete History", "status": 200, "data": HistoryDelete})
