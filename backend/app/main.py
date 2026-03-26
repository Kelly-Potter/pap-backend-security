from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.app.security import hash_password, verify_password, create_access_token
from backend.app.users import fake_users_db

app = FastAPI(
    title="PAP Security Backend",
    description="Backend para detecao de logins suspeitos",
    version="0.1.0"
)

# Modelo de dados
class User(BaseModel):
    username: str
    password: str

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# REGISTO
@app.post("/register")
def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    fake_users_db[user.username] = {
        "username": user.username,
        "password": hashed
    }

    return {"message": "User created"}

# LOGIN
@app.post("/login")
def login(user: User):
    db_user = fake_users_db.get(user.username)

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    return {"access_token": token}
