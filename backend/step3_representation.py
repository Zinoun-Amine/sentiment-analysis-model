import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import joblib
import os

def step3_representation_and_split():
    """ÉTAPE 3: Représentation vectorielle (TF-IDF) et division des données"""
    
    print("🔢 ÉTAPE 3: REPRÉSENTATION VECTORIELLE (TF-IDF)")
    print("="*60)
    
    # 1. CHARGEMENT DES DONNÉES PRÉTRAITÉES
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'data', 'processed', 'tiktok_preprocessed.csv')
    
    df = pd.read_csv(data_path)
    
    # Supprimer les lignes avec du texte vide (juste au cas où)
    df.dropna(subset=['text_processed'], inplace=True)
    
    print(f"📊 Dataset chargé: {len(df):,} avis")
    
    # 2. PRÉPARATION DES DONNÉES (X et y)
    print("\n🔄 Préparation des données pour la modélisation...")
    
    # X: Le texte traité (nos features)
    X = df['text_processed']
    
    # y: Les sentiments (nos cibles)
    y = df['sentiment']
    
    print(f"   • X (textes): {X.shape[0]} exemples")
    print(f"   • y (sentiments): {y.shape[0]} labels")
    
    # 3. CRÉATION DE LA MATRICE TF-IDF
    print("\n🔠 Création des features TF-IDF...")
    
    # Initialiser le vectoriseur TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=5000,      # Garder les 5000 mots les plus importants
        ngram_range=(1, 2),     # Considérer les mots seuls (unigrammes) et les paires de mots (bigrammes)
        min_df=5                # Ignorer les mots qui apparaissent dans moins de 5 avis
    )
    
    # Appliquer le vectoriseur sur nos textes
    X_tfidf = vectorizer.fit_transform(X)
    
    print(f"✅ Matrice TF-IDF créée avec succès!")
    print(f"   • Forme de la matrice: {X_tfidf.shape[0]} lignes × {X_tfidf.shape[1]} features")
    print(f"   • Nombre de mots dans le vocabulaire: {len(vectorizer.get_feature_names_out())}")
    
    # Afficher quelques features
    print(f"   • Exemples de features: {list(vectorizer.get_feature_names_out())[2000:2010]}")
    
    # 4. DIVISION DES DONNÉES (Train / Test)
    print("\n🔪 Division des données en ensembles d'entraînement et de test...")
    
    # 80% pour l'entraînement, 20% pour le test
    X_train, X_test, y_train, y_test = train_test_split(
        X_tfidf, 
        y, 
        test_size=0.2, 
        random_state=42,
        stratify=y  # Important pour garder la même proportion de sentiments dans train et test
    )
    
    print(f"✅ Données divisées:")
    print(f"   • Entraînement: {X_train.shape[0]:,} exemples")
    print(f"   • Test: {X_test.shape[0]:,} exemples")
    
    # 5. SAUVEGARDER LES DONNÉES ET LE VECTORIZER
    print("\n💾 Sauvegarde des données et du vectorizer pour l'étape 4...")
    
    output_dir = os.path.join(base_dir, 'data', 'processed')
    
    # Sauvegarder les ensembles de données
    joblib.dump(X_train, os.path.join(output_dir, 'X_train.pkl'))
    joblib.dump(X_test, os.path.join(output_dir, 'X_test.pkl'))
    joblib.dump(y_train, os.path.join(output_dir, 'y_train.pkl'))
    joblib.dump(y_test, os.path.join(output_dir, 'y_test.pkl'))
    
    # Sauvegarder le vectorizer (très important pour l'API)
    models_dir = os.path.join(base_dir, 'data', 'models')
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(vectorizer, os.path.join(models_dir, 'tfidf_vectorizer.pkl'))
    
    print(f"   • Fichiers de données sauvegardés dans: {output_dir}")
    print(f"   • Vectorizer sauvegardé dans: {models_dir}")
    
    print(f"\n🎯 Prêt pour l'ÉTAPE 4: CLASSIFICATION")
    
    return True

if __name__ == "__main__":
    step3_representation_and_split()