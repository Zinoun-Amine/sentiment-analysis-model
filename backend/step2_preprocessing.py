import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import emoji
import os
from collections import Counter
import matplotlib.pyplot as plt

# Télécharger les ressources NLTK nécessaires
def setup_nltk():
    """Télécharge les ressources NLTK nécessaires"""
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print(" Téléchargement des ressources NLTK...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)

class TextPreprocessor:
    
    def __init__(self):
        setup_nltk()
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.tiktok_words = {'tiktok', 'app', 'video', 'content', 'creator', 'fyp', 'viral'}
        self.stop_words = self.stop_words - self.tiktok_words
        
    def clean_text(self, text):
        """Nettoie le texte des avis"""
        if pd.isna(text):
            return ""
        
        text = str(text)
        
        # 1. Convertir les emojis en texte
        text = emoji.demojize(text, delimiters=(" ", " "))
        
        # 2. Convertir en minuscules
        text = text.lower()
        
        # 3. Supprimer les URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\$$\$$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # 4. Supprimer les mentions (@username)
        text = re.sub(r'@\w+', '', text)
        
        # 5. Supprimer les hashtags mais garder le texte
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # 6. Supprimer les caractères spéciaux mais garder la ponctuation importante
        text = re.sub(r'[^\w\s!?.]', ' ', text)
        
        # 7. Supprimer les chiffres isolés
        text = re.sub(r'\b\d+\b', '', text)
        
        # 8. Supprimer les espaces multiples
        text = ' '.join(text.split())
        
        return text.strip()
    
    def tokenize_and_lemmatize(self, text):
        """Tokenise et lemmatise le texte"""
        if not text:
            return []
        
        # Tokenisation
        tokens = word_tokenize(text)
        
        # Supprimer la ponctuation et les mots courts
        tokens = [token for token in tokens if token not in string.punctuation and len(token) > 2]
        
        # Supprimer les stop words
        tokens = [token for token in tokens if token not in self.stop_words]
        
        # Lemmatisation
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return tokens
    
    def preprocess_text(self, text):
        """Pipeline complet de prétraitement"""
        # Nettoyage
        cleaned = self.clean_text(text)
        
        # Tokenisation et lemmatisation
        tokens = self.tokenize_and_lemmatize(cleaned)
        
        # Rejoindre les tokens
        processed = ' '.join(tokens)
        
        return processed

def step2_preprocessing():
    """ÉTAPE 2: Prétraitement des textes d'avis TikTok"""
    
    print("🧹 ÉTAPE 2: PRÉTRAITEMENT DES TEXTES")
    print("="*60)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'data', 'processed', 'tiktok_sentiment_data.csv')
    
    df = pd.read_csv(data_path)
    print(f"📊 Dataset chargé: {len(df):,} avis")
    sample_size = min(50000, len(df))  # Limiter à 50k pour les tests
    df_sample = df.sample(n=sample_size, random_state=42)
    print(f"📝 Échantillon de travail: {len(df_sample):,} avis")
    
    preprocessor = TextPreprocessor()
    print(f"\n EXEMPLES DE PRÉTRAITEMENT:")
    
    sample_texts = [
        "I LOVE THIS APP!!! 😍😍😍 Best app ever!!!",
        "This app is terrible... so many bugs 😡",
        "TikTok is okay, not bad but could be better 🤷‍♀️",
        "Can't even sign in!!! Fix your app @tiktok #frustrated",
        "Great content and videos! Very addictive app 🔥"
    ]
    
    for i, text in enumerate(sample_texts, 1):
        cleaned = preprocessor.clean_text(text)
        processed = preprocessor.preprocess_text(text)
        
        print(f"\n   {i}. Original: {text}")
        print(f"      Nettoyé:  {cleaned}")
        print(f"      Traité:   {processed}")
    
    # 2. TRAITEMENT DE TOUT LE DATASET
    print(f"\n🔄 Traitement de l'échantillon...")
    
    # Ajouter les versions nettoyées et traitées
    df_sample['text_cleaned'] = df_sample['text'].apply(preprocessor.clean_text)
    df_sample['text_processed'] = df_sample['text'].apply(preprocessor.preprocess_text)
    
    # Supprimer les textes vides après traitement
    df_clean = df_sample[df_sample['text_processed'].str.len() > 0].copy()
    print(f"✅ Après nettoyage: {len(df_clean):,} avis utilisables")
    
    # 3. STATISTIQUES POST-TRAITEMENT
    print(f"\n📊 STATISTIQUES POST-TRAITEMENT:")
    
    # Longueur des textes
    original_lengths = df_clean['text'].str.len()
    processed_lengths = df_clean['text_processed'].str.len()
    
    print(f"   📏 Longueur moyenne:")
    print(f"      • Originale: {original_lengths.mean():.1f} caractères")
    print(f"      • Traitée:   {processed_lengths.mean():.1f} caractères")
    
    # Distribution par sentiment
    print(f"\n   😊 Distribution finale:")
    sentiment_dist = df_clean['sentiment'].value_counts()
    for sentiment, count in sentiment_dist.items():
        percentage = (count / len(df_clean)) * 100
        print(f"      • {sentiment}: {count:,} ({percentage:.1f}%)")
    
    # 4. ANALYSE DES MOTS LES PLUS FRÉQUENTS
    print(f"\n🔤 MOTS LES PLUS FRÉQUENTS PAR SENTIMENT:")
    
    for sentiment in ['positive', 'negative', 'neutral']:
        texts = df_clean[df_clean['sentiment'] == sentiment]['text_processed']
        all_words = ' '.join(texts).split()
        
        if all_words:
            word_freq = Counter(all_words)
            top_words = word_freq.most_common(10)
            
            print(f"\n   📱 {sentiment.upper()}:")
            for word, freq in top_words:
                print(f"      • {word}: {freq:,}")
    
    # 5. SAUVEGARDER LES DONNÉES PRÉTRAITÉES
    output_path = os.path.join(base_dir, 'data', 'processed', 'tiktok_preprocessed.csv')
    
    # Garder les colonnes importantes
    df_final = df_clean[['text', 'text_cleaned', 'text_processed', 'sentiment', 'score']].copy()
    df_final.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"\n DONNÉES PRÉTRAITÉES SAUVEGARDÉES:")
    print(f"    Fichier: {output_path}")
    print(f"    Dataset final: {len(df_final):,} avis")
    print(f"    Prêt pour l'ÉTAPE 3: REPRÉSENTATION")
    
    return df_final

if __name__ == "__main__":
    df = step2_preprocessing()
