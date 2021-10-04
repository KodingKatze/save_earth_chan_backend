from __future__ import annotations
import datetime
import os, json
from flask_cors import CORS
from dataclasses import dataclass
from flask import Flask, request, jsonify
from  models import setup_db, Disaster, db_drop_and_create_all, db

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.name = "Save Earth-chan"
    app.config['JSON_SORT_KEYS'] = False
    setup_db(app)
    CORS(app)
    """ uncomment at the first time running the app """

    @dataclass
    class ErrorResponse:
        Error: str
        Api: str

        def toJson(cls):
            return {
                "error": cls.Error,
                "api": cls.Api
            }

    @dataclass
    class SuccessResponse:
        Task: str
        Api: str

        def toJson(cls):
            return {
                "task": cls.Task,
                "api": cls.Api
            }

    # ROOT API
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'message': 'SAVE EARTH CHANNN!!'})

    # GET ALL DATA OR INSERT DATA
    @app.route("/api/disaster", methods=["POST", "GET"])
    def addDisaster():
        if (request.method == "GET"):
            Data = [ds for ds in Disaster.query.order_by(Disaster.id).all()]
            return jsonify([objDis.toJson() for objDis in Data])
            # return json.dumps(Data)
        elif (request.method == "POST"):
            try:
                disaster = request.get_json()

                NewDisaster = Disaster(
                    EventTitle=disaster.get("title"),
                    Description=disaster.get("desc"),
                    Location=disaster.get("loc"),
                    Pictures=disaster.get("pics")
                )
                NewDisaster.insert()

                return jsonify(SuccessResponse(
                    Task="Disaster has been added!",
                    Api="addDisaster"
                ).toJson())
            except Exception as e:
                return jsonify(ErrorResponse(
                    Error=e,
                    Api="addDisaster"
                ).toJson())

    # GET DATA BY ID
    @app.route("/api/disaster/<id>", methods=["GET"])
    def getDisasterById(id):
        disGet = Disaster.query.get(id)
        if str(disGet.id) == id:
            return jsonify(disGet.toJson())

        return jsonify(ErrorResponse(
            "Not Found!",
            "getDisasterById:{}".format(id)
        ).toJson())

    return app

app = create_app()
