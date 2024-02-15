from fastapi import APIRouter
from models.petsday import Petsday
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId
import hashlib
import secrets

SECRET_KEY = secrets.token_urlsafe(32)



router = APIRouter()
@router.get("/")
async def get_petsdays():
  petsdays = list_serial(collection_name.find())
  return petsdays

@router.post("/")
async def post_petsday(petsday:Petsday):
   collection_name.insert_one(dict(petsday))
@router.put("/{id}")
async def put_petsday(id: str, petsday:Petsday):
 collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(petsday)})
@router.delete("/{id}")
async def delete_petsday(id: str):
  collection_name.find_one_and_delete({"_id":ObjectId(id)})

@router.post("/register")
async def register_user(petsday: Petsday):
    # Rastgele bir tuz oluşturun
    salt = secrets.token_hex(16)  # 16 byte uzunluğunda bir rastgele tuz oluşturur

    # Kullanıcının parolasını ve tuzunu birleştirip hashleyelim
    hashed_password = hashlib.sha256((petsday.password + salt).encode()).hexdigest()

    # Tuzlu ve hashlenmiş parolayı kullanarak yeni bir Petsday nesnesi oluşturun.
    new_petsday = Petsday(
        username=petsday.username,
        email=petsday.email,
        password=hashed_password,
        salt=salt  # Tuzu kaydetmek için
    )

    # Veritabanına yeni kullanıcıyı ekleyin.
    collection_name.insert_one(dict(new_petsday))

    # Başarılı bir şekilde kaydedildiğine dair bir mesaj döndürün.
    return {"message": "User registered successfully"}