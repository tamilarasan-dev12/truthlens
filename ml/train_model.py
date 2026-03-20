import csv
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline

try:
    from ml.features import LinguisticFeatures
except ModuleNotFoundError:
    from features import LinguisticFeatures


MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "statements.csv"


def _fallback_samples():
    return [
        ("NASA confirms discovery of water traces on Mars in recent mission report.", "True"),
        ("World Health Organization releases annual influenza trend summary for 2025.", "True"),
        ("Federal Reserve published updated economic projections after latest meeting.", "True"),
        ("University research team publishes peer-reviewed climate adaptation findings.", "True"),
        ("City council approves new public transportation funding after public vote.", "True"),
        ("Hospital network reports reduction in emergency wait times after staffing changes.", "True"),
        ("National weather service issues storm advisory with expected rainfall estimates.", "True"),
        ("Energy agency data shows gradual increase in renewable electricity output.", "True"),
        ("Court releases official statement clarifying timeline of hearing proceedings.", "True"),
        ("Education board announces revised curriculum guidelines for upcoming school year.", "True"),
        ("Breaking: secret cure for every disease hidden by global doctors.", "Fake"),
        ("Government replaces all gasoline with invisible fuel starting next month.", "Fake"),
        ("Aliens sign trade deal with world leaders according to anonymous source.", "Fake"),
        ("Drinking one herb tea instantly reverses aging by twenty years.", "Fake"),
        ("Social media post proves moon is made of synthetic concrete.", "Fake"),
        ("Scientists admit gravity is optional for people with strong mindset.", "Fake"),
        ("Hidden code in smartphone updates lets authorities read every thought.", "Fake"),
        ("Single vitamin tablet can permanently boost IQ by seventy points.", "Fake"),
        ("Famous actor secretly elected president of three different countries.", "Fake"),
        ("Ancient prophecy predicts internet shutdown caused by underwater volcano tomorrow.", "Fake"),
        ("Public health bulletin confirms vaccine efficacy rates through independent trials.", "True"),
        ("Central bank minutes detail concerns over inflation and labor market trends.", "True"),
        ("Rail authority publishes safety audit and maintenance completion statistics.", "True"),
        ("Major newspaper retracts fabricated quote after editorial investigation.", "True"),
        ("Cybersecurity agency warns organizations about phishing campaigns this quarter.", "True"),
        ("One click now reveals absolute truth behind every political speech.", "Fake"),
        ("Ocean disappears overnight according to viral unverified satellite screenshot.", "Fake"),
        ("Celebrity-owned crystal device guarantees immunity from all viruses forever.", "Fake"),
        ("Leaked memo claims every election result was prewritten decades ago.", "Fake"),
        ("Mysterious frequency from radio towers controls human decision making daily.", "Fake"),
    ]


def _load_from_csv(path):
    if not path.exists():
        return []

    samples = []
    with path.open("r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            text = (row.get("text") or row.get("statement") or "").strip()
            label = (row.get("label") or row.get("prediction") or "").strip().title()
            if text and label in {"Fake", "True"}:
                samples.append((text, label))
    return samples


def load_training_data():
    samples = _load_from_csv(DATA_PATH)
    if len(samples) < 20:
        samples = _fallback_samples()

    texts = [item[0] for item in samples]
    labels = [item[1] for item in samples]
    return texts, labels


def build_pipeline():
    features = FeatureUnion(
        transformer_list=[
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    max_features=5000,
                    lowercase=True,
                    strip_accents="unicode",
                ),
            ),
            ("linguistic", LinguisticFeatures()),
        ]
    )

    classifier = RandomForestClassifier(
        n_estimators=320,
        random_state=42,
        n_jobs=1,
        class_weight="balanced",
    )

    return Pipeline(
        steps=[
            ("features", features),
            ("classifier", classifier),
        ]
    )


def train_and_save_model(model_path=MODEL_PATH):
    texts, labels = load_training_data()
    pipeline = build_pipeline()
    pipeline.fit(texts, labels)

    output_path = Path(model_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, output_path)
    return output_path


if __name__ == "__main__":
    saved_path = train_and_save_model()
    print(f"Model saved to: {saved_path}")
