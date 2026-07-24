from pydantic import BaseModel, field_validator
from typing import Dict, Any

from app.utils.feature_validation import FEATURE_LIMITS


class PredictionRequest(BaseModel):

    features: Dict[str, Any]

    @field_validator("features")
    @classmethod
    def validate_feature_ranges(cls, values):


        for feature, value in values.items():


            if feature not in FEATURE_LIMITS:
                continue

            if not isinstance(value, (int, float)):
                continue

            limits = FEATURE_LIMITS[feature]


            if value < limits["min"]:

                raise ValueError(
                    f"{feature} inférieur au minimum autorisé ({limits['min']})"
                )

            if value > limits["max"]:

                raise ValueError(
                    f"{feature} supérieur au maximum autorisé ({limits['max']})"
                )

        return values



class PredictionResponse(BaseModel):

    client_id: int
    probability_default: float
    threshold: float
    decision: int
