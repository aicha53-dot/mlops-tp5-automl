
# Modèle manuel ou modèle AutoML ? — TP05

## 1. Objectif

Comparer le modèle Random Forest entraîné manuellement avec le modèle XGBoost sélectionné automatiquement par FLAML.

Les deux modèles sont évalués sur le même jeu de test de 1 250 transactions et sont servis localement avec MLflow.

## 2. Tableau comparatif

| Critère | Manuel (RF 500/16) | AutoML (FLAML 90 s) |
|---|---|---|
| Famille de modèle | Random Forest | XGBoost |
| F1 sur le jeu de test | 0.8669 | 0.8582 |
| Temps machine | 1.0 s (entraînement) | 91.2 s (recherche) |
| Temps humain | Non chronométré (TP02) | Non chronométré |
| Latence médiane - essai 1 | 37.4 ms | 24.8 ms |
| Latence médiane - essai 2 | 40.1 ms | 23.5 ms |
| Latence p95 - essai 1 | 58.2 ms | 34.9 ms |
| Latence p95 - essai 2 | 65.5 ms | 39.8 ms |
| Taille du fichier | 13.37 Mio | 0.29 Mio |
| Explicabilité | Importance des variables, 500 arbres, profondeur max. 16 | Importance des variables, 333 estimateurs, complexité limitée |

## 3. Analyse des résultats

Le Random Forest obtient le meilleur F1-score avec 0.8669, contre 0.8582 pour XGBoost.

Cependant, XGBoost présente une latence inférieure dans les deux campagnes de mesure.

Le modèle AutoML est également beaucoup plus compact : 0.29 Mio contre 13.37 Mio pour le modèle manuel.

Les deux modèles permettent d'étudier l'importance des variables et d'analyser leurs structures d'arbres.

La durée de recherche AutoML et le temps d'entraînement manuel ne mesurent pas exactement la même opération.

## 4. Décision de production

Nous retenons XGBoost AutoML comme candidat au déploiement dans notre scénario local.
Son F1-score de 0.8582 reste proche de celui du Random Forest (0.8669).
Ses latences médianes sont plus faibles dans les deux campagnes de mesure.
Sa taille de 0.29 Mio facilite le stockage et le déploiement.
Avant un usage bancaire réel, il faudrait confirmer ce choix par l'analyse des faux négatifs, du rappel et des coûts métier.
