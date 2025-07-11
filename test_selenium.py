# Fichier : test_selenium.py

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

TIKTOK_URL = "https://www.tiktok.com/@salmakml1/video/7513603225887509766"

print("--- DÉBUT DU SCRIPT DE DIAGNOSTIC SELENIUM ---")

edge_options = EdgeOptions()
# IMPORTANT : On ne met PAS headless pour voir la fenêtre s'ouvrir
edge_options.add_argument("--inprivate")

# Assurez-vous que msedgedriver.exe est dans ce dossier
service = EdgeService(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service, options=edge_options)

try:
    print(f"1. Navigation vers : {TIKTOK_URL}")
    driver.get(TIKTOK_URL)
    
    print("2. Attente de 15 secondes pour que la page se charge complètement...")
    time.sleep(15)

    print("3. Recherche de TOUTES les balises <span> sur la page...")
    
    # On cherche tous les spans, sans distinction. C'est un test "brute force".
    all_spans = driver.find_elements(By.TAG_NAME, 'span')
    
    if not all_spans:
        print("--- RÉSULTAT : AUCUNE balise <span> n'a été trouvée. C'est le cœur du problème.")
    else:
        print(f"--- RÉSULTAT : {len(all_spans)} balises <span> trouvées ! ---")
        print("Voici le texte des 20 premières balises non vides :")
        
        count = 0
        for i, span in enumerate(all_spans):
            if count >= 20:
                break
            
            # .text est la propriété qui contient le texte visible
            span_text = span.text
            
            if span_text: # Si le texte n'est pas vide
                print(f"  - Span #{i+1}: '{span_text}'")
                count += 1

except Exception as e:
    print(f"--- UNE ERREUR EST SURVENUE --- : {e}")
finally:
    print("\nFermeture du navigateur.")
    driver.quit()
    print("--- FIN DU SCRIPT ---")