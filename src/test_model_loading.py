import pandas as pd

from model_loader import load_model


model = load_model()


X_test = pd.read_parquet(
    "./notebooks/X_test_ml.parquet"
)


sample = X_test.iloc[[0]]


prediction = model.predict(sample)


print("Prediction :", prediction)
