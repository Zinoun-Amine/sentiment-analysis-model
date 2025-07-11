import nltk
import ssl

def download_nltk_resources():
    """Télécharge toutes les ressources NLTK nécessaires"""
    
    # Contourner les problèmes SSL
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    print("📥 Téléchargement des ressources NLTK...")
    
    resources = [
        'punkt',
        'punkt_tab',
        'stopwords', 
        'wordnet',
        'omw-1.4',
        'averaged_perceptron_tagger'
    ]
    
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
            print(f"✅ {resource}")
        except Exception as e:
            print(f"❌ {resource}: {e}")
    
    print("🎉 Ressources NLTK installées!")

if __name__ == "__main__":
    download_nltk_resources()