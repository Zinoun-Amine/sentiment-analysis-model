import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_tiktok_content():
    print("🔍 ANALYSE APPROFONDIE DES DONNÉES TIKTOK")
    print("="*60)
    
    # Charger les données
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, 'data', 'tiktok_google_play_reviews.csv')
    
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"📊 Dataset: {len(df):,} avis")
    print(f"\n ANALYSE DES SCORES:")
    score_counts = df['score'].value_counts().sort_index()
    
    for score, count in score_counts.items():
        percentage = (count / len(df)) * 100
        bar = "█" * int(percentage / 2)  
        print(f"   {score} étoiles: {count:7,} ({percentage:5.1f}%) {bar}")

    def score_to_sentiment(score):
        if score >= 4:
            return 'positive'
        elif score <= 2:
            return 'negative'
        else:
            return 'neutral'
    
    df['sentiment'] = df['score'].apply(score_to_sentiment)
    
    print(f"\n😊 DISTRIBUTION DES SENTIMENTS:")
    sentiment_counts = df['sentiment'].value_counts()
    
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(df)) * 100
        emoji = {'positive': '😊', 'negative': '😞', 'neutral': '😐'}[sentiment]
        print(f"   {emoji} {sentiment:8}: {count:7,} ({percentage:5.1f}%)")
    
    df_content = df.dropna(subset=['content'])
    print(f"\n📝 ANALYSE DU CONTENU:")
    print(f"   • Avis avec contenu: {len(df_content):,}")
    print(f"   • Avis sans contenu: {len(df) - len(df_content):,}")

    content_lengths = df_content['content'].str.len()
    print(f"\n📏 LONGUEUR DES AVIS:")
    print(f"   • Moyenne: {content_lengths.mean():.0f} caractères")
    print(f"   • Médiane: {content_lengths.median():.0f} caractères")
    print(f"   • Min: {content_lengths.min()}")
    print(f"   • Max: {content_lengths.max()}")
    print(f"   • Plus de 100 caractères: {(content_lengths > 100).sum():,}")
    print(f"   • Moins de 20 caractères: {(content_lengths < 20).sum():,}")
 
    print(f"\n🔍 EXEMPLES D'AVIS PAR SENTIMENT:")
    
    for sentiment in ['positive', 'negative', 'neutral']:
        examples = df_content[df_content['sentiment'] == sentiment].head(3)
        print(f"\n📱 AVIS {sentiment.upper()}:")
        
        for i, (_, row) in enumerate(examples.iterrows(), 1):
            content = row['content'][:120] + "..." if len(row['content']) > 120 else row['content']
            print(f"   {i}. {row['score']} - {row['userName']}")
            print(f"      💬 {content}")
            print(f"      👍 {row['thumbsUpCount']} likes")
    
    print(f"\n👥 ANALYSE DES UTILISATEURS:")
    user_counts = df['userName'].value_counts()
    print(f"   • Utilisateurs uniques: {len(user_counts):,}")
    print(f"   • Utilisateurs avec plus d'1 avis: {(user_counts > 1).sum():,}")
    print(f"   • Max avis par utilisateur: {user_counts.max()}")
 
    print(f"\n👍 ANALYSE DES LIKES:")
    thumbs_stats = df['thumbsUpCount'].describe()
    print(f"   • Moyenne de likes: {thumbs_stats['mean']:.1f}")
    print(f"   • Médiane de likes: {thumbs_stats['50%']:.0f}")
    print(f"   • Max likes: {thumbs_stats['max']:.0f}")
    print(f"\n🎯 PRÉPARATION POUR L'ANALYSE DE SENTIMENTS:")
    
    df_clean = df_content[df_content['content'].str.len() >= 10].copy()
    print(f"   • Avis avec au moins 10 caractères: {len(df_clean):,}")
    
    final_sentiment_dist = df_clean['sentiment'].value_counts()
    print(f"   • Distribution finale:")
    for sentiment, count in final_sentiment_dist.items():
        percentage = (count / len(df_clean)) * 100
        print(f"     - {sentiment}: {count:,} ({percentage:.1f}%)")
    
    output_dir = os.path.join(base_dir, 'data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    
    final_dataset = df_clean[['content', 'score', 'sentiment', 'userName', 'thumbsUpCount']].copy()
    final_dataset = final_dataset.rename(columns={'content': 'text'})
    
    output_path = os.path.join(output_dir, 'tiktok_sentiment_data.csv')
    final_dataset.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"\n DONNÉES PRÉPARÉES POUR L'ANALYSE DE SENTIMENTS:")
    print(f"   Fichier: {output_path}")
    print(f"   Dataset final: {len(final_dataset):,} avis")
    print(f"   Prêt pour l'ÉTAPE 2: PRÉTRAITEMENT")
    
    return final_dataset

if __name__ == "__main__":
    df = analyze_tiktok_content()