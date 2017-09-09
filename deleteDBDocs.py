import pymongo

client = pymongo.MongoClient("mongodb://admin:admin@firstresponse-shard-00-00-u0yzh.mongodb.net:27017,firstresponse-shard-00-01-u0yzh.mongodb.net:27017,firstresponse-shard-00-02-u0yzh.mongodb.net:27017/test?ssl=true&replicaSet=firstResponse-shard-0&authSource=admin")
db = client.firstResponse
db.firstResponders
db.victims

resultResponders = db.firstResponders.delete_many({})
print (resultResponders.deleted_count, "first responder documents have been deleted")
resultVictims = db.victims.delete_many({})
print (resultVictims.deleted_count, "victim documents have been delted")
