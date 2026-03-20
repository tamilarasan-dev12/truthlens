import os
import joblib
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from load_data import load_and_preprocess_data
from ML.custom_transformers import LinguisticFeatureExtractor

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')

def train():
    print("Loading data...")
    df = load_and_preprocess_data()
    X = df['statement']
    y = df['label']
    
    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Advanced NLP Pipeline with FeatureUnion
    print("Building advanced FeatureUnion pipeline...")
    pipeline = Pipeline([
        ('features', FeatureUnion([
            ('tfidf', TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                max_features=5000,
                sublinear_tf=True
            )),
            ('linguistic', LinguisticFeatureExtractor())
        ])),
        ('clf', RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            random_state=42,
            class_weight='balanced'
        ))
    ])
    
    print("Training the RandomForest FeatureUnion model...")
    pipeline.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print("Classification Report:\n", report)
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, 'model.pkl')
    joblib.dump(pipeline, model_path)
    print(f"\nAdvanced FeatureUnion model successfully trained and saved to {model_path}.")

if __name__ == '__main__':
    train()
