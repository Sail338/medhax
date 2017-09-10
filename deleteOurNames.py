import pymongo

client = pymongo.MongoClient("mongodb://admin:admin@firstresponse-shard-00-00-u0yzh.mongodb.net:27017,firstresponse-shard-00-01-u0yzh.mongodb.net:27017,firstresponse-shard-00-02-u0yzh.mongodb.net:27017/test?ssl=true&replicaSet=firstResponse-shard-0&authSource=admin")
db = client.firstResponse
db.firstResponders
db.victims

sriResponders = db.firstResponders.delete_one({"name": "Sri"})
sriResponders = db.firstResponders.delete_one({"name": "sri"})
sriResponders = db.firstResponders.delete_one({"name": "Ranga"})
sriResponders = db.firstResponders.delete_one({"name": "ranga"})
sriResponders = db.firstResponders.delete_one({"name": "Alice"})
sriResponders = db.firstResponders.delete_one({"name": "alice"})
print (sriResponders.deleted_count, "first responder documents have been deleted")

sriResponders = db.victims.delete_one({"name": "Sri"})
sriResponders = db.victims.delete_one({"name": "sri"})
sriResponders = db.victims.delete_one({"name": "Ranga"})
sriResponders = db.victims.delete_one({"name": "ranga"})
sriResponders = db.victims.delete_one({"name": "Alice"})
sriResponders = db.victims.delete_one({"name": "alice"})
print (resultVictims.deleted_count, "victim documents have been delted")
