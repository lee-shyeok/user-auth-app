from sklearn.ensemble import RandomForestClassifier
import numpy as np

def predict_health_risk(age: int, bmi: float, blood_pressure: int, cholesterol: int) -> dict:
    risk_score = 0
    
    if age > 50:
        risk_score += 2
    elif age > 35:
        risk_score += 1
    
    if bmi > 30:
        risk_score += 2
    elif bmi > 25:
        risk_score += 1
    
    if blood_pressure > 140:
        risk_score += 2
    elif blood_pressure > 120:
        risk_score += 1
    
    if cholesterol > 240:
        risk_score += 2
    elif cholesterol > 200:
        risk_score += 1

    if risk_score >= 5:
        level = "고위험"
    elif risk_score >= 3:
        level = "중위험"
    else:
        level = "저위험"

    return {"risk_score": risk_score, "risk_level": level}