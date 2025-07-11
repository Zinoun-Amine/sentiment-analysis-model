import pandas as pd
import os

def explore_csv_file():
    
    print(" ÉTAPE 1: EXPLORATION DES DONNÉES")
    print("="*50)
    base_dir = os.path.dirname(os.path.dirname(__file__))  
    csv_path = os.path.join(base_dir, 'data', 'tiktok_google_play_reviews.csv')
    
    print(f"📁 Fichier: {csv_path}")
    if not os.path.exists(csv_path):
        print(" Fichier non trouvé!")
        return

    file_size = os.path.getsize(csv_path) / (1024 * 1024)  # en MB
    print(f" Taille du fichier: {file_size:.2f} MB")
    print("\n Chargement du fichier...")
    try:
        df = pd.read_csv(csv_path)
        print(f"Fichier chargé avec succès!")
        print(f"\n INFORMATIONS DE BASE:")
        print(f"   • Nombre de lignes: {len(df):,}")
        print(f"   • Nombre de colonnes: {len(df.columns)}")
    
        print(f"\n COLONNES:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. {col}")
        
        print(f"\n APERÇU (3 premières lignes):")
        print(df.head(3))
        print(f"\n🔧 TYPES DE DONNÉES:")
        for col in df.columns:
            print(f"   • {col}: {df[col].dtype}")

        print(f"\n VALEURS MANQUANTES:")
        missing = df.isnull().sum()
        for col in df.columns:
            if missing[col] > 0:
                print(f"   • {col}: {missing[col]:,} ({missing[col]/len(df)*100:.1f}%)")
        
        return df
        
    except Exception as e:
        print(f" Erreur lors du chargement: {e}")
        return None

if __name__ == "__main__":
    df = explore_csv_file()
    if df is not None:
        print(f"\n Exploration terminée!")
        print(f" Dataset: {len(df):,} lignes × {len(df.columns)} colonnes")