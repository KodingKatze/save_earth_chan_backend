from __future__ import annotations
import datetime
import os, json
from flask_cors import CORS
from dataclasses import dataclass
from sqlalchemy import or_
from flask import Flask, request, jsonify, sessions
from sqlalchemy.sql.expression import select
from models import setup_db, Disaster, QueryType, db_drop_and_create_all, db

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
   
   @app.route('/api')
   def easterEgg():
      return jsonify({'message': "Kyan! EARTH-chwan inside!"})
   # GET ALL DATA
   @app.route("/api/disaster", methods=["GET"])
   def getDisasterAll():
      try:
         itemPerPage = int(request.args.get("perPage", 10))
         page = int(request.args.get("page", 1))

         Data = [ds for ds in Disaster.query
                              .order_by(Disaster.id)
                              .limit(itemPerPage)
                              .offset(page-1)]
         return jsonify([objDis.toJson() for objDis in Data])
      
      except Exception as e:
         return jsonify(ErrorResponse(
               Error=e.args,
               Api="getDisasterAll"
         ).toJson())

   # INSERT DATA
   @app.route("/api/disaster", methods=["POST"])
   def addDisaster():
      try:
         disaster: dict = request.get_json()

         NewDisaster = Disaster(
               EventTitle=disaster.get("eventTitle"),
               Description=disaster.get("description"),
               Location=disaster.get("location"),
               Pictures=disaster.get("picture"),
               Latitude=disaster.get("latitude"),
               Longitude=disaster.get("longitude"),
               Category=list(tag.lower() for tag in disaster["category"]) if disaster["category"] else None
         )
         print(NewDisaster)
         # NewDisaster.insert()

         return jsonify(SuccessResponse(
               Task="Disaster has been added!",
               Api="addDisaster"
         ).toJson())
      except Exception as e:
         return jsonify(ErrorResponse(
               Error=e.args,
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

   @app.route("/api/disaster/search", methods=["GET"])
   def searchTitle():
      query = request.args.get("query", type=QueryType)
      category = request.args.get("category", type=QueryType)
      
      itemPerPage = request.args.get("perPage", 10, type=int)
      page = request.args.get("page", 1, type=int)

      data = [ds for ds in Disaster.query
               .filter(
                  Disaster.EventTitle.ilike(f'%{query}%') | 
                  Disaster.Description.ilike(f'%{query}%') | 
                  Disaster.Category.contains([category])
                  )
               .limit(itemPerPage)
               .offset(page-1)]
      return jsonify([objDis.toJson() for objDis in data])
      
app = create_app()
