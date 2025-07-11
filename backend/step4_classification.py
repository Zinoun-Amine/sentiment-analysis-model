import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import time

def step5_1_balanced_model_training():
    """ÉTAPE 5.1: Entraînement d'un modèle pondéré pour corriger le déséquilibre."""
    
    print("🤖 ÉTAPE 5.1: AMÉLIORATION DU MODÈLE (PONDÉRATION)")
    print("="*60)
    
    # --- 1. CHARGEMENT DES DONNÉES ---
    # Garde la même structure de chemin que votre script original
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(base_dir, 'data', 'processed')
        models_dir = os.path.join(base_dir, 'data', 'models')
        # S'assurer que le dossier des modèles existe
        os.makedirs(models_dir, exist_ok=True)
    except NameError:
        # __file__ n'est pas défini si vous exécutez dans un notebook interactif
        # Remplacez par votre chemin de base si nécessaire
        print("Avertissement: __file__ non défini. Utilisation d'un chemin relatif de base.")
        base_dir = '.'
        data_dir = os.path.join(base_dir, 'data', 'processed')
        models_dir = os.path.join(base_dir, 'data', 'models')


    print("🔄 Chargement des données d'entraînement et de test...")
    X_train_path = os.path.join(data_dir, 'X_train.pkl')
    X_test_path = os.path.join(data_dir, 'X_test.pkl')
    y_train_path = os.path.join(data_dir, 'y_train.pkl')
    y_test_path = os.path.join(data_dir, 'y_test.pkl')
    
    try:
        X_train = joblib.load(X_train_path)
        X_test = joblib.load(X_test_path)
        y_train = joblib.load(y_train_path)
        y_test = joblib.load(y_test_path)
    except FileNotFoundError as e:
        print(f"\n❌ ERREUR: Impossible de charger les fichiers de données.")
        print(f"   Vérifiez que les fichiers .pkl existent dans le dossier '{data_dir}'")
        print(f"   Détail: {e}")
        return False
    
    print(f"   • Entraînement: {X_train.shape[0]} exemples")
    print(f"   • Test: {X_test.shape[0]} exemples")
    
    # --- 2. DÉFINITION ET ENTRAÎNEMENT DU MODÈLE PONDÉRÉ ---
    print("\n🚀 Entraînement du modèle: Logistic Regression (Pondéré)...")
    
    # LA MODIFICATION CLÉ EST ICI: class_weight='balanced'
    # Cela pénalise les erreurs sur les classes minoritaires (negative, neutral)
    model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    
    # Entraînement
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time
    print(f"   • Entraînement terminé en {training_time:.2f} secondes.")
    
    # Prédiction sur l'ensemble de test
    start_time = time.time()
    y_pred = model.predict(X_test)
    prediction_time = time.time() - start_time
    print(f"   • Prédiction terminée en {prediction_time:.2f} secondes.")
    
    # --- 3. ÉVALUATION DÉTAILLÉE DU NOUVEAU MODÈLE ---
    print("\n🏆 ÉVALUATION DU MODÈLE PONDÉRÉ")
    print("="*60)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"   • ✅ Nouvelle Accuracy: {accuracy:.2%}")
    print("      (Note: Une légère baisse de l'accuracy est normale et attendue)")

    # Afficher le rapport détaillé du nouveau modèle
    print("\n📊 NOUVEAU RAPPORT DE CLASSIFICATION DÉTAILLÉ:")
    # Vos labels semblent être 'negative', 'neutral', 'positive'
    class_labels = ['negative', 'neutral', 'positive']
    # Nous utilisons y_test.unique() pour être sûr de l'ordre des labels si jamais il change
    # Mais il faut s'assurer que l'ordre correspond bien aux labels attendus.
    # Pour plus de robustesse, on peut mapper les entiers (ex: 0, 1, 2) aux noms.
    # Supposons l'ordre : 0=negative, 1=neutral, 2=positive
    
    print(classification_report(y_test, y_pred, target_names=class_labels, digits=2))

    print("\n--- Analyse des Résultats ---")
    print("Comparez ces scores (surtout 'recall' et 'f1-score' pour 'negative' et 'neutral')")
    print("avec ceux de votre modèle précédent pour voir l'amélioration de l'équilibre.")
    
    # --- 4. SAUVEGARDE DU MODÈLE AMÉLIORÉ ---
    # On donne un nouveau nom au modèle pour ne pas écraser l'ancien
    model_path = os.path.join(models_dir, 'best_sentiment_model_balanced.pkl')
    joblib.dump(model, model_path)
    
    print(f"\n💾 Modèle amélioré 'Logistic Regression (Pondéré)' sauvegardé dans: {model_path}")
    print(f"   Ce modèle est une meilleure base pour l'API.")
    
    print(f"\n🎯 Prêt pour l'analyse des résultats et potentiellement l'étape SMOTE.")
    
    return True

if __name__ == "__main__":
    # On appelle directement notre nouvelle fonction
    step5_1_balanced_model_training()