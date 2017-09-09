import pymongo

client = pymongo.MongoClient("mongodb://admin:admin@firstresponse-shard-00-00-u0yzh.mongodb.net:27017,firstresponse-shard-00-01-u0yzh.mongodb.net:27017,firstresponse-shard-00-02-u0yzh.mongodb.net:27017/test?ssl=true&replicaSet=firstResponse-shard-0&authSource=admin")
db = client.firstResponse
db.firstResponders
db.victims

def addResponder( responderDictionary ):
    if not responderDictionary.has_key("Name"):
        break
    if not responderDictionary.has_key("Location"):
        break
    db.firstResponders.insert_one(responderDictionary)

def addVictim( victimDictionary ):
    if not victimDictionary.has_key("Name"):
        break
    if not victimDictionary.has_key("Location"):
        break
    db.victims.insert_one(victimDictionary)

#db.firstResponders.insert_one({"Name": "test", "location": {"latitude": 50, "longitude": 50}})
