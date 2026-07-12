from mlflow import MlflowClient


def load_threshold():

    client = MlflowClient(
        tracking_uri="http://127.0.0.1:5000"
    )

    model_version = client.get_model_version_by_alias(
        "P06_LightGBM_Optimized",
        "champion"
    )

    run = client.get_run(
        model_version.run_id
    )

    return run.data.metrics["best_threshold"]
