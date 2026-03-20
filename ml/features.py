import re

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


WORD_RE = re.compile(r"\b\w+\b")
PUNCT_RE = re.compile(r"[^\w\s]")


class LinguisticFeatures(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        vectors = []
        for raw_text in X:
            text = (raw_text or "").strip()
            text_length = float(len(text))

            punct_count = len(PUNCT_RE.findall(text))
            punctuation_density = punct_count / max(text_length, 1.0)

            words = WORD_RE.findall(text)
            avg_word_length = (
                sum(len(word) for word in words) / len(words) if words else 0.0
            )

            vectors.append([text_length, punctuation_density, avg_word_length])

        return np.asarray(vectors, dtype=float)
