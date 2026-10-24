
from fastapi import FastAPI, HTTPException
from app.schemas import PredictionRequest
from app.predict import predict_default, model, feature_columns
from app.database import get_connection
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(
    title="Credit Risk Assessment API",
    description="Predict credit default risk using XGBoost",
    version="1.0.0")
@app.get("/")
def home():
    return {
        "message": "Credit Risk Assessment API is running"}
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "number_of_features": len(feature_columns)}
@app.get("/predictions")
def get_predictions():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, prediction, risk_label,default_probability, created_at
                FROM prediction_history
                ORDER BY created_at DESC
            """)
            rows = cur.fetchall()
    return [
        {
        "id": row[0],
        "prediction": row[1],
        "risk_label": row[2],
        "default_probability": float(row[3]),
        "created_at": row[4]
        }for row in rows]
@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        result = predict_default(request.features)
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                """
                INSERT INTO prediction_history
                (prediction, risk_label, default_probability)
                VALUES (%s, %s, %s)
                """,
            (
            result["prediction"],
            result["risk_label"],
            result["default_probability"]
            )
        )
        return result
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error))
