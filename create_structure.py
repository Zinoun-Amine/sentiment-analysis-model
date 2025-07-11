import os

# Structure des dossiers et fichiers
structure = {
    'backend': {
        'data_collection': ['__init__.py', 'tiktok_scraper.py', 'data_manager.py'],
        'preprocessing': ['__init__.py', 'text_cleaner.py', 'data_augmentation.py'],
        'feature_extraction': ['__init__.py', 'text_vectorizer.py', 'feature_engineering.py'],
        'models': ['__init__.py', 'sentiment_classifier.py', 'model_trainer.py', 'model_evaluator.py'],
        'api': ['__init__.py', 'app.py', 'routes.py', 'utils.py'],
        'config': ['config.py']
    },
    'data': {
        'raw': [],
        'processed': [],
        'models': []
    }
}

# Créer la structure
for main_folder, subfolders in structure.items():
    for subfolder, files in subfolders.items():
        # Créer le chemin complet
        folder_path = os.path.join(main_folder, subfolder)
        os.makedirs(folder_path, exist_ok=True)
        
        # Créer les fichiers
        for file in files:
            file_path = os.path.join(folder_path, file)
            open(file_path, 'w').close()

# Créer requirements.txt
open('backend/requirements.txt', 'w').close()

print("✅ Structure créée avec succès!")