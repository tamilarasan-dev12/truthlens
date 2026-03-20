import string
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class LinguisticFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Extracts linguistic metadata features from a list of strings:
    - Token Count (word count)
    - Average Word Length
    - Punctuation Density (%)
    """
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        features = []
        for doc in X:
            words = doc.split()
            word_count = len(words)
            if word_count == 0:
                features.append([0, 0, 0])
                continue
                
            avg_word_length = sum(len(word) for word in words) / word_count
            
            punct_count = sum(1 for char in doc if char in string.punctuation)
            punct_density = (punct_count / len(doc)) * 100 if len(doc) > 0 else 0
            
            features.append([word_count, avg_word_length, punct_density])
            
        return np.array(features)
