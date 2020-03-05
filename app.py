from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pprint import pprint
from bson.json_util import loads
import json
import datetime
app = Flask(__name__)

client = MongoClient()
db = client.WhoLetTheDogsOut
meteorites = db.meteorites
meteorites.delete_many({})

with open("meteorites.json", 'r') as file:
    data = json.load(file)
    for member in data:
        id = meteorites.insert_one(loads(json.dumps(member)))
        print(id)

@app.route("/")
def home():
    return findName("Aachen")


def findName(name):
        for meteorite in meteorites.find({"name" : str(name)}):
                pprint(meteorite)


def findMass(mass):
        for meteorite in meteorites.find({"mass": str(mass)}):
                pprint(meteorite)


def findYear(year):
        i = 0
        for meteorite in meteorites.find():
                try:
                        yeartemp = meteorite["year"][:4]
                        if (yeartemp == str(year)):
                                pprint(meteorite)
                except: pass


def findCoordinates(lat, long):
        for meteorite in meteorites.find({"$and":[
                        {"reclat" : { "$gt": str(lat-2), "$lt": str(lat+2)}},
                        {"reclong" : { "$gt": str(long-2), "$lt": str(long+2)}}
                        ]}):
                pprint(meteorite)


if __name__ == "__main__":
    app.debug = True
    app.run()
