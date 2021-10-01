from __future__ import annotations
from typing import List

from dataclasses import dataclass
from flask import Flask, request, jsonify

@dataclass
class Disaster:
    EventId: str
    EventTitle: str
    Description: str = None
    Location: str = None
    Pictures: List(str) = None

    def toJson(cls):
        return {
            "eventId": cls.EventId,
            "eventTitle": cls.EventTitle,
            "description": cls.Description,
            "location": cls.Location,
            "pictures": cls.Pictures or None
        }

@dataclass
class DisasterList:
    Data: List[Disaster]
    Count: int

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

app = Flask("Save Earth-chan")
app.config['JSON_SORT_KEYS'] = False

disasterDB = DisasterList(
    Data = [
        Disaster("E001", "Weebification", "Manifestation of despaired weeb attempt to fight back society", "Mars", None),
        Disaster("E002", "Global Horny", "Everthing looks hot", "Global", None)
    ],
    Count= 2
)

@app.route("/api/disaster", methods=["GET"])
def getDisasterAll():
    return jsonify([ds.toJson() for ds in disasterDB.Data])

@app.route("/api/disaster", methods=["POST"])
def addDisaster():
    try:
        disaster = request.get_json()

        disasterDB.Data.append(Disaster(
            EventId='E{:03}'.format(disasterDB.Count+1),
            EventTitle=disaster.get("title"),
            Description= disaster.get("desc"),
            Location= disaster.get("loc"),
            Pictures= disaster.get("pics")
        ))
    except Exception as e:
        return jsonify(ErrorResponse(
            Error=e,
            Api="addDisaster"
        ).toJson())
    else:
        disasterDB.Count += 1
        return jsonify(SuccessResponse(
            Task="Disaster has been added!",
            Api="addDisaster"
        ).toJson())

@app.route("/api/disaster/<id>", methods=["GET"])
def getDisasterById(id):
    for d in disasterDB.Data:
        if d.EventId == id:
            return jsonify(d.toJson())
    return jsonify(ErrorResponse(
        "Not Found!",
        "getDisasterById:{}".format(id)
    ).toJson())

app.run(debug=True)