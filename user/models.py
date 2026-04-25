from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from database.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class HealthProfile(Base):
    __tablename__ = "health_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    age = Column(Integer)
    bmi = Column(Float)
    blood_pressure = Column(Integer)
    cholesterol = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)