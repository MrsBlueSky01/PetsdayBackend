from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
import hashlib  # Hashleme için hashlib kütüphanesini kullanacağız.

from models.petsday import Petsday

app = FastAPI()

# Kullanıcıların depolanacağı bir sözlük kullanalım.
users_db = {}

# JWT için bir anahtar belirleyelim.
SECRET_KEY = "mysecretkey"


# Kullanıcı bilgilerini tutmak için bir BaseModel tanımlayalım.


# Kullanıcı kaydı yapmak için bir endpoint tanımlayalım.



@app.post("/register")
async def register(user: Petsday):
    # Kullanıcı adı zaten kullanımda mı kontrol edelim.
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Kullanıcının parolasını hashleyelim.
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    # Kullanıcı bilgilerini güncelleyelim ve parolanın hashlenmiş versiyonunu saklayalım.
    users_db[user.username] = {"username": user.username, "email": user.email, "password": hashed_password}

    # Kullanıcıya JWT oluşturalım.
    token = jwt.encode({"username": user.username}, SECRET_KEY, algorithm="HS256")

    # JWT'yi kullanıcıya geri dönelim.
    return {"token": token}
