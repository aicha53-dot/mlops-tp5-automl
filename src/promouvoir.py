import sys
import mlflow
from mlflow import MlflowClient

# Nom du modele passe en argument
nom = sys.argv[1]

# Connexion au serveur MLflow
mlflow.set_tracking_uri('http://127.0.0.1:5000')

client = MlflowClient()

# Rechercher les versions du modele
versions = client.search_model_versions(
    f"name='{nom}'"
)

# Identifier la derniere version
derniere = max(
    int(v.version) for v in versions
)

# Attribuer l'alias production
client.set_registered_model_alias(
    nom,
    'production',
    str(derniere)
)

print(
    f'{nom} : version {derniere} '
    'promue (alias production)'
)