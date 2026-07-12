import mlflow.sklearn


MODEL_URI = "models:/P06_LightGBM_Optimized@champion"


def load_model():

    mlflow.set_tracking_uri(
        "http://127.0.0.1:5000"
    )

    return mlflow.sklearn.load_model(
            MODEL_URI
            )
