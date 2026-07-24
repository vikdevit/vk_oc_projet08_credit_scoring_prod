import pytest

from app.schemas import PredictionRequest
from app.utils.feature_validation import FEATURE_LIMITS


def test_all_features_valid_min_max():

    for feature, limits in FEATURE_LIMITS.items():

        # valeur normale au milieu des bornes
        value = (
            limits["min"] + limits["max"]
        ) / 2

        PredictionRequest(
            features={
                feature: value
            }
        )



def test_all_features_reject_below_min():

    for feature, limits in FEATURE_LIMITS.items():

        with pytest.raises(ValueError):

            PredictionRequest(
                features={
                    feature: limits["min"] - 1
                }
            )



def test_all_features_reject_above_max():

    for feature, limits in FEATURE_LIMITS.items():

        with pytest.raises(ValueError):

            PredictionRequest(
                features={
                    feature: limits["max"] + 1
                }
            )
