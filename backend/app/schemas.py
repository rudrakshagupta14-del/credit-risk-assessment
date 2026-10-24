
from pydantic import BaseModel, Field
class PredictionRequest(BaseModel):
    features: dict[str, float] = Field(...,description="Here are all 23 Customer features used by the model")
    model_config={
        "json_schema_extra":{
            "example":{
                "features":{
                    "LIMIT_BAL": 50000,
                    "SEX": 1,
                    "EDUCATION": 2,
                    "MARRIAGE": 1,
                    "AGE": 30,
                    "PAY_0": 2,
                    "PAY_2": 2,
                    "PAY_3": 1,
                    "PAY_4": 1,
                    "PAY_5": 0,
                    "PAY_6": 0,
                    "BILL_AMT1": 48000,
                    "BILL_AMT2": 46000,
                    "BILL_AMT3": 43000,
                    "BILL_AMT4": 40000,
                    "BILL_AMT5": 35000,
                    "BILL_AMT6": 30000,
                    "PAY_AMT1": 1000,
                    "PAY_AMT2": 1000,
                    "PAY_AMT3": 1500,
                    "PAY_AMT4": 2000,
                    "PAY_AMT5": 2500,
                    "PAY_AMT6": 3000                   
                }
            }
        }
    }
