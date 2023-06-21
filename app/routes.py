from app import app
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import  userController, historyController, predictControler


@app.route('/user', methods=['GET', 'PUT'])
@jwt_required()
def userDetails():
    current_user = get_jwt_identity()
    if(request.method == 'GET'):
        return userController.getDetailUser(current_user)
    if(request.method == 'PUT'):
        return userController.updateUser(current_user)


@app.route('/signup', methods=['POST'])
def signUp():
    return userController.signUp()


@app.route('/signin', methods=['POST'])
def signIn():
    return userController.signIn()

@app.route('/hypoxia', methods=['POST'])
def predict():
    return predictControler.calculate_hypoxia()

@app.route('/history', methods=['POST','GET'])
@jwt_required()
def history():
    payload_user = get_jwt_identity()
    if(request.method == 'POST'):
        return historyController.postHistory(payload_user)
    elif(request.method == 'GET'):
        return historyController.getAllHistory(payload_user)   

@app.route('/history/<id>', methods=['DELETE'])
@jwt_required()
def historyById(id):
    return historyController.deleteHistory(id)