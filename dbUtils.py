import pymongo
import googlemaps
from geopy.distance import vincenty


client = pymongo.MongoClient("mongodb://admin:admin@firstresponse-shard-00-00-u0yzh.mongodb.net:27017,firstresponse-shard-00-01-u0yzh.mongodb.net:27017,firstresponse-shard-00-02-u0yzh.mongodb.net:27017/test?ssl=true&replicaSet=firstResponse-shard-0&authSource=admin")
db = client.firstResponse
db.firstResponders
db.victims

def addResponder( responderDictionary ):
    if "name" not in responderDictionary:
        return
    if "location" not in responderDictionary:
        return
    if "phone" not in responderDictionary:
        return
    db.firstResponders.insert_one(responderDictionary)

def addVictim( victimDictionary ):  #adds victim to db and then retuns tuple of the distance to the nearest responder and their name
    if "name" not in victimDictionary:
        return
    if "location" not in victimDictionary:
        return
    if "phone" not in victimDictionary:
        return
    db.victims.insert_one(victimDictionary)
    return findNearestResponder(victimDictionary)

def findNearestResponder( victimDictionary ):
    loc = victimDictionary["location"]
    closestResponder = ()

    for item in db.firstResponders.find():
        responderLoc = (item["location"]["lat"], item["location"]["lat"])
        dist = vincenty(loc, responderLoc).miles
        if not closestResponder:
            closestResponder = (dist, item)
        elif dist < closestResponder[0]:
            closestResponder = (dist, item)

    return closestResponder

def addTestResponder( name, location, phone ):
    lat = location[0]
    lng = location[1]

    db.firstResponders.insert_one({"name": name, "location": {"lat": lat, "lng": lng}, "phone": phone})

name = "Ranga"
loc = (10, 50)
phone = 7329978242
addTestResponder(name, loc, phone)
