import jwt
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta

# MongoDB'ye bağlanma
client = MongoClient("mongodb+srv://kuruyyaren:Yaren0905@cluster0.p3pey0o.mongodb.net/?retryWrites=true&w=majority")
db = client.petsday_db
collection_name = db["petsday_collection"]

# Kullanıcı kaydı
def register(username, password, email):
    # Kullanıcı var mı kontrol edin
    if collection_name.find_one({"username": username}):
        return False  # Kullanıcı zaten varsa False döndür
    # Yeni kullanıcıyı veritabanına ekleyin
    collection_name.insert_one({"username": username, "password": password, "email": email})
    return True  # Kayıt başarılıysa True döndür

# Kullanıcı girişi
def login(username, password):
    # Kullanıcıyı bulun
    user = collection_name.find_one({"username": username, "password": password})
    if user:
        # Kullanıcı adı ve parola doğruysa JWT token üretin ve döndürün
        token_payload = {
            "user_id": str(user["_id"]),  # Kullanıcı kimliğini JWT içinde saklayın
            "exp": datetime.utcnow() + timedelta(days=1)  # Token geçerlilik süresi (örneğin 1 gün)
        }
        return jwt.encode(token_payload, 'secret', algorithm='HS256')  # JWT token'i döndür
    else:
        return None  # Kullanıcı adı veya parola yanlışsa None döndür

# Örnek kullanım
if __name__ == "__main__":
    username = input("Kullanıcı adınızı girin: ")
    password = input("Parolanızı girin: ")

    # Kullanıcı kaydı
    if register(username, password, "example@example.com"):
        print("Kullanıcı başarıyla kaydedildi.")

    # Kullanıcı girişi
    token = login(username, password)
    if token:
        print("JWT token:", token)
    else:
        print("Kullanıcı adı veya parola yanlış.")


def individual_serial(petsday)->dict:
    return {
     "id": str(petsday["_id"]),
     "username": petsday["username"],
     "password": petsday["password"],
     "email": petsday["email"],
 }
def list_serial(petsdays)-> list:
    return [individual_serial(petsday) for petsday in petsdays]