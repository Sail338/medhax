import pymongo
import googlemaps
from geopy.distance import vicenity


client = pymongo.MongoClient("mongodb://admin:admin@firstresponse-shard-00-00-u0yzh.mongodb.net:27017,firstresponse-shard-00-01-u0yzh.mongodb.net:27017,firstresponse-shard-00-02-u0yzh.mongodb.net:27017/test?ssl=true&replicaSet=firstResponse-shard-0&authSource=admin")
db = client.firstResponse
db.firstResponders
db.victims

def addResponder( responderDictionary ):
    if not responderDictionary.has_key("name"):
        break
    if not responderDictionary.has_key("location"):
        break
    if not responderDictionary.has_key("phone"):
        break
    db.firstResponders.insert_one(responderDictionary)

def addVictim( victimDictionary ):  #adds victim to db and then retuns tuple of the distance to the nearest responder and their name
    if not victimDictionary.has_key("name"):
        break
    if not victimDictionary.has_key("location"):
        break
    if not victimDictionary.has_key("phone"):
        break
    db.victims.insert_one(victimDictionary)
    return findNearestResponder(victimDictionary)

def findNearestResponder( victimDictionary )
    loc = victimDictionary["location"]
    closestResponder = ()

    for item in db.firstResponders.find():
        responderLoc = (item["location"]["lat"], item["locatoin"]["lat"])
        dist = vicenity(loc, responderLoc).miles
        if not closestResponder:
            closestResponder = (dist, item)
        elif dist < closestResponder[0]:
            closestResponder = (dist, item)

    return closestResponder


#db.firstResponders.insert_one({"name": "test", "location": {"lat": 50, "lng": 50}})
