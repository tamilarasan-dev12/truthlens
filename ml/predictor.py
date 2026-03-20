from pathlib import Path
from threading import Lock

import joblib

try:
    from ml.features import LinguisticFeatures  # noqa: F401
    from ml.train_model import MODEL_PATH, train_and_save_model
except ModuleNotFoundError:
    from features import LinguisticFeatures  # noqa: F401
    from train_model import MODEL_PATH, train_and_save_model


class TruthLensPredictor:
    def __init__(self, model_path=None):
        self.model_path = Path(model_path or MODEL_PATH)
        self._model = None
        self._lock = Lock()
        self._load_model()

    @staticmethod
    def _normalize_label(value):
        return "Fake" if str(value).strip().lower() == "fake" else "True"

    def _load_model(self):
        with self._lock:
            if self._model is not None:
                return
            if not self.model_path.exists():
                train_and_save_model(self.model_path)
            self._model = joblib.load(self.model_path)

    def predict(self, text):
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")

        self._load_model()
        clean_text = text.strip()

        predicted_raw = self._model.predict([clean_text])[0]
        prediction = self._normalize_label(predicted_raw)

        prob_vector = self._model.predict_proba([clean_text])[0]
        class_labels = [self._normalize_label(label) for label in self._model.classes_]

        probabilities = {"Fake": 0.0, "True": 0.0}
        for label, score in zip(class_labels, prob_vector):
            probabilities[label] = float(score)

        confidence = float(probabilities.get(prediction, max(probabilities.values())))

        return {
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "probabilities": {
                "Fake": round(float(probabilities["Fake"]), 4),
                "True": round(float(probabilities["True"]), 4),
            },
        }


_PREDICTOR = None
_PREDICTOR_LOCK = Lock()


def get_predictor():
    global _PREDICTOR
    with _PREDICTOR_LOCK:
        if _PREDICTOR is None:
            _PREDICTOR = TruthLensPredictor()
    return _PREDICTOR
