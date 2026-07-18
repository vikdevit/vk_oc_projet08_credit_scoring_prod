# script d'écriture dans la table reference_stats des données statistiques de référence de X_train

import pandas as pd

from sqlalchemy.orm import Session

from app.database.connection import engine
from app.database.session import SessionLocal

from app.models.reference_stats import ReferenceStats


X_TRAIN_PATH = "data/X_train_ml.parquet"


def compute_reference():

    print("Chargement X_train...")

    df = pd.read_parquet(
        X_TRAIN_PATH
    )

    print(
        "Dimensions :",
        df.shape
    )


    db = SessionLocal()

    print("Nettoyage de reference_stats...")

    #db.query(ReferenceStats).delete()
    #db.commit()


    print("Calcul statistiques...")


    for column in df.columns:

        stats = ReferenceStats(

            feature_name=column,

            mean_value=float(
                df[column].mean()
            ),

            std_value=float(
                df[column].std()
            ),

            min_value=float(
                df[column].min()
            ),

            max_value=float(
                df[column].max()
            ),

            sample_size=int(
                len(df)
            )
        )


        db.add(stats)


    db.commit()

    db.close()


    print(
        "Référence X_train enregistrée"
    )


if __name__ == "__main__":

    compute_reference()
