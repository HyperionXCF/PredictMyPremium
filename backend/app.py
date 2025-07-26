from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

# Tier cities
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120)]
    weight: Annotated[float, Field(..., gt=0, lt=150)]
    height: Annotated[float, Field(..., gt=0, lt=2.5)]
    income_lpa: Annotated[float, Field(..., gt=0)]
    smoker: Annotated[bool, Field(...)]
    user_city: Annotated[str, Field(..., alias="user_city")]
    occupation: Annotated[Literal["business_owner", "private_job", "retired", "unemployed"], Field(...)]

    @computed_field(return_type=float)
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field(return_type=str)
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker and self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field(return_type=str)
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"

@app.post("/predict")
def predict_premium(data: UserInput):
    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city": 1 if data.user_city.capitalize() in tier_1_cities else 2 if data.user_city.capitalize() in tier_2_cities else 3,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation.lower()
    }])
    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content={"predicted_category": prediction})
