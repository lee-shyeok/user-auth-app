from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from dotenv import load_dotenv
from database.db import engine, get_db, Base
from user.models import User, HealthProfile
from auth.jwt import verify_password, get_password_hash, create_access_token, decode_token
from prediction.model import predict_health_risk

load_dotenv()
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class HealthInput(BaseModel):
    age: int
    bmi: float
    blood_pressure: int
    cholesterol: int

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    if result.scalar():
        raise HTTPException(status_code=400, detail="이미 존재하는 유저입니다")
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(new_user)
    await db.commit()
    return {"message": "회원가입 완료!"}

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form.username))
    user = result.scalar()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
async def me(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return {"username": payload.get("sub")}

@app.post("/health/predict")
async def predict(data: HealthInput, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    username = payload.get("sub")
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar()

    profile = HealthProfile(
        user_id=user.id,
        age=data.age,
        bmi=data.bmi,
        blood_pressure=data.blood_pressure,
        cholesterol=data.cholesterol
    )
    db.add(profile)
    await db.commit()

    prediction = predict_health_risk(data.age, data.bmi, data.blood_pressure, data.cholesterol)
    return {"username": username, **prediction}