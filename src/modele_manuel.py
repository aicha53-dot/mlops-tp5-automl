import time
from pathlib import Path
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

# 1. Charger les donnees
df = pd.read_csv('data/transactions.csv')

X = df.drop(columns='fraude')
y = df['fraude']

# 2. Meme decoupage que le modele AutoML
Xtr, Xte, ytr, yte = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42
)

# 3. Entrainer le modele manuel du TP02
t0 = time.time()

modele = RandomForestClassifier(
    n_estimators=500,
    max_depth=16,
    random_state=42
).fit(Xtr, ytr)

duree = round(time.time() - t0, 1)

# 4. Evaluer le modele
f1 = round(f1_score(yte, modele.predict(Xte)), 4)

# 5. Sauvegarder une copie locale
Path('models').mkdir(exist_ok=True)
joblib.dump(modele, 'models/model_manuel.pkl')

print(
    'modele manuel : F1 =',
    f1,
    '| entrainement',
    duree,
    's'
)

# 6. Enregistrer dans MLflow
mlflow.set_tracking_uri('http://127.0.0.1:5000')
mlflow.set_experiment('tp5-automl-deploiement')

with mlflow.start_run(run_name='manuel-rf-500-16'):

    mlflow.log_params({
        'outil': 'scikit-learn',
        'n_estimators': 500,
        'max_depth': 16
    })

    mlflow.log_metrics({
        'f1': f1,
        'duree_entrainement_s': duree
    })

    info = mlflow.sklearn.log_model(
        modele,
        name='model',
        input_example=Xte.head(3),
        registered_model_name='fraude-manuel',
        serialization_format='skops',
        skops_trusted_types=['sklearn.tree._tree.Tree']
    )

print(
    'enregistre : fraude-manuel, version',
    info.registered_model_version
)