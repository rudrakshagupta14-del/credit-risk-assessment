
import joblib
import pandas as pd
from app.config import MODEL_PATH, COLUMNS_PATH
# Load the saved model and columns
model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(COLUMNS_PATH)
def predict_default(features: dict):
    # Check that all required features are present
    missing = [col for col in feature_columns if col not in features]

    if missing:
        raise ValueError(
            f"Missing features: {missing}"
        )
    # Check that no unexpected features are provided
    extra = [col for col in features if col not in feature_columns]
    if extra:
        raise ValueError(
            f"Unexpected features: {extra}"
        )
    # Arrange input columns in training order
    input_df = pd.DataFrame(
        [[features[col] for col in feature_columns]],
        columns=feature_columns
    )
    # Predict default class
    prediction = int(model.predict(input_df)[0])
    # Get probability for class 1 (default)
    probabilities = model.predict_proba(input_df)[0]
    class_index = list(model.classes_).index(1)
    probability = float(probabilities[class_index])
    return {
        "prediction": prediction,
        "risk_label": (
            "Default predicted" if prediction == 1 else "No default predicted"
        ),
        "default_probability": round(probability, 4)
    }
