from __future__ import annotations
import json
import requests
from datetime import datetime
from flask_cors import CORS
from dataclasses import dataclass
from sqlalchemy import or_, and_
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
         ).toJson()), 400

   # INSERT DATA
   @app.route("/api/disaster", methods=["POST"])
   def addDisaster():
      try:
         disaster: dict = json.loads(request.form.get("data"))
         pics = request.files
         imageList = []
         
         if pics: 
            for _, img in pics.items():
               res = uploadImage(img.stream)
               if res:
                  imageList.append(res)
            if len(imageList): 
               disaster["picture"] = imageList
         else:
            disaster["picture"] = None

         NewDisaster = Disaster(
               EventTitle=disaster.get("eventTitle"),
               Description=disaster.get("description"),
               Location=disaster.get("location"),
               Pictures=disaster.get("picture"),
               Latitude=float(disaster.get("latitude")),
               Longitude=float(disaster.get("longitude")),
               Category=list(tag.lower() for tag in disaster["category"]) if disaster["category"] else None
         )
         NewDisaster.insert()

         return jsonify(SuccessResponse(
               Task="Disaster has been added!",
               Api="addDisaster"
         ).toJson())
      except Exception as e:
         print(e)
         return jsonify(ErrorResponse(
               Error=e.args,
               Api="addDisaster"
         ).toJson()), 400

   # GET DATA BY ID
   @app.route("/api/disaster/<id>", methods=["GET"])
   def getDisasterById(id):
      try:
         disGet = Disaster.query.get(id)
         if str(disGet.id) == id:
            return jsonify(disGet.toJson())
      except Exception as e:
         return jsonify(ErrorResponse(
            "Not Found!",
            "getDisasterById:{}".format(id)
         ).toJson()), 400

   @app.route("/api/disaster/search", methods=["GET"])
   def searchTitle():
      try:
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
      
      except Exception as e:
         return jsonify(ErrorResponse(
            "Not Found!",
            "getDisasterById:{}".format(id)
         ).toJson()), 400
   
   @app.route("/api/disaster/nearMe", methods=["GET"])
   def searchNearMe():
      try:
         latitude = request.args.get("latitude", type=float)
         longitude = request.args.get("longitude", type=float)

         page = request.args.get("page", 1, type=int)
         itemPerPage = request.args.get("perPage", type=int)
         data = [ds for ds in Disaster.query
                  .filter(
                     absoulute(Disaster.Latitude - latitude) <= 1.0 &
                     absoulute(Disaster.Longitude - longitude) <= 1.0
                  )
                  .limit(itemPerPage)
                  .offset(page-1)]
         return jsonify([objDis.toJson() for objDis in data])

      except Exception as e:
         return jsonify(ErrorResponse(
            "Not Found!",
            "getDisasterById:{}".format(id)
         ).toJson()), 400

   def uploadImage(data) -> str:
      res = requests.post("https://api.imgbb.com/1/upload", params={
         'key': '00a1aeca97124c2ddb0ace6f0bc4fffc',
      }, files={
         'image': data.read()
      }).json()

      if res.get("status") == 200:
         return res.get("data").get("url")
      else:
         return None

   def absoulute(val) -> int:
      return val if val > 0 else val*-1

   return app

app = create_app()
