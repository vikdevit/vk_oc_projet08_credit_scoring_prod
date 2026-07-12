import mlflow
import pandas as pd


# Connexion MLflow
mlflow.set_tracking_uri(
    "http://127.0.0.1:5000"
)


# Chargement modèle champion
model = mlflow.pyfunc.load_model(
    "models:/P06_LightGBM_Optimized@champion"
)


# Chargement vrai dataset
X_test = pd.read_parquet(
    "./notebooks/X_test_ml.parquet"
)


print("Shape X_test :", X_test.shape)

print("Colonnes :", len(X_test.columns))


# Prendre une seule ligne de test
sample = X_test.iloc[[0]]


print("Shape sample :", sample.shape)


# Prédiction
prediction = model.predict(sample)


print("Prediction :", prediction)
