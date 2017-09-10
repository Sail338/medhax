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
    loc = (victimDictionary["location"]["lat"], victimDictionary["location"]["lng"])
    closestResponder = ()

    for item in db.firstResponders.find():
        responderLoc = (item["location"]["lat"], item["location"]["lng"])
        dist = vincenty(loc, responderLoc).miles
        if not closestResponder:
            closestResponder = (dist, item)
        elif dist < closestResponder[0]:
            closestResponder = (dist, item)
    return closestResponder

def findNearestVictim( responderDictionary ):
    loc = (responderDictionary["location"]["lat"], responderDictionary["location"]["lng"])
    closestVictim = ()

    for item in db.victims.find():
        victimLoc = (item["location"]["lat"], item["location"]["lng"])
        dist = vincenty(loc, victimLoc).miles
        if not closestVictim:
            closestVictim = (dist, item)
        elif dist < closestVictim[0]:
            closestVictim = (dist, item)
    return closestVictim

def getVictimLocations():
    victimLocations = []
    for item in db.victims.find():
        loc = {"lat":item["location"]["lat"], "lng":item["location"]["lng"]}
        victimLocations.append( loc )
    return victimLocations

def getResponderLocations():
    responderLoc = []
    for item in db.firstResponders.find():
        loc = {"lat":item["location"]["lat"], "lng":item["location"]["lng"]}
        responderLoc.append( loc )
    return responderLoc

def deleteVictim( name ):
    db.victims.delete_one({"name": name})

def addPerson( name, lat, lng, phone, isVictim ):   #requires boolean isVictim to be true for victim insert and false for responder insert
    if isVictim:
        db.victims.insert_one({"name": name, "location": {"lat": lat, "lng": lng}, "phone": phone})
    else:
        db.firstResponders.insert_one({"name": name, "location": {"lat": lat, "lng": lng}, "phone": phone})

def addTestResponder( name, location, phone ):
    lat = location[0]
    lng = location[1]
    db.firstResponders.insert_one({"name": name, "location": {"lat": lat, "lng": lng}, "phone": phone})
