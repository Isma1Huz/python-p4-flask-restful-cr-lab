#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):

    def get(self):
        plants = Plant.query.all()

        response_dict = [all.to_dict() for all in plants]

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response
    def post(self):
        data = Plant(
            name=request.json['name'],
            image=request.json['image'],
            price=request.json['price']
        )

        db.session.add(data)
        db.session.commit()

        response_dict = data.to_dict()

        response = make_response(
            jsonify(response_dict),
            201
        )

        return response

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant_by_id = Plant.query.filter_by(id=id).first().to_dict()

        response =make_response(
            jsonify(plant_by_id),
            200
        )      
        return response


api.add_resource(PlantByID, '/plants/<int:id>')  

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)
