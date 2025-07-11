
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from config.config import Config

def display_evaluation_metrics(y_true, y_pred, model_name="Model"):

    print(f"\n📊 Classification Report for {model_name}:\n")
    report = classification_report(
        y_true, y_pred, target_names=Config.SENTIMENT_CLASSES, zero_division=0
    )
    print(report)

    print("Generating confusion matrix...")
    cm = confusion_matrix(y_true, y_pred, labels=Config.SENTIMENT_CLASSES)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=Config.SENTIMENT_CLASSES, 
                yticklabels=Config.SENTIMENT_CLASSES)
    plt.title(f'Confusion Matrix for {model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show() 

    return report