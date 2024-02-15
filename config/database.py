from pymongo import MongoClient

client = MongoClient("mongodb+srv://kuruyyaren:Yaren0905@cluster0.p3pey0o.mongodb.net/?retryWrites=true&w=majority")
db = client.petsday_db
collection_name=db["petsday_collection"]