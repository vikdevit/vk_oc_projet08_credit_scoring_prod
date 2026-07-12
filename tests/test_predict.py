import json
import pytest

from app.predictor import predict

def test_predict_client_ok(client):

    with open(
        "data/sample_request_client_ok.json"
    ) as f:

        payload = json.load(f)


    response = client.post(
        "/predict",
        json={
            "features": payload
        }
    )


    assert response.status_code == 200


    result = response.json()


    assert "client_id" in result
    assert "probability_default" in result
    assert "threshold" in result
    assert "decision" in result


    assert result["decision"] in [0,1]

def test_predict_client_risk(client):

    with open(
        "data/sample_request_client_risk.json"
    ) as f:

        payload = json.load(f)


    response = client.post(
        "/predict",
        json={
            "features": payload
        }
    )


    assert response.status_code == 200


    result = response.json()


    assert result["decision"] == 1

import pytest

from app.predictor import predict


def test_predict_missing_features():

    bad_features = {
        "SK_ID_CURR": 100005
    }

    with pytest.raises(Exception):

        predict(bad_features)
