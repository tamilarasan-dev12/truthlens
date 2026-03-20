import re
from html import unescape
from urllib import error as urllib_error
from urllib import request as urllib_request
from urllib.parse import urlparse

from flask import current_app

from database.db import get_db
from database.models import (
    fetch_dashboard_metrics,
    fetch_history_rows,
    insert_history_row,
)
from ml.predictor import get_predictor


class InputValidationError(ValueError):
    pass


class ExternalContentError(RuntimeError):
    pass


def _looks_like_url(value):
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _clean_html(raw_html):
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", raw_html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _fetch_url_text(url):
    timeout = current_app.config.get("REQUEST_TIMEOUT_SECONDS", 8)
    try:
        req = urllib_request.Request(
            url,
            headers={"User-Agent": "TruthLens/1.0 (+https://localhost)"},
        )
        with urllib_request.urlopen(req, timeout=timeout) as response:
            charset = response.headers.get_content_charset("utf-8")
            body = response.read().decode(charset, errors="replace")
    except (urllib_error.URLError, ValueError) as exc:
        raise ExternalContentError(f"Failed to fetch URL: {exc}") from exc

    extracted = _clean_html(body)
    if len(extracted) < 40:
        raise ExternalContentError("URL content is too short to analyze.")
    return extracted


def _resolve_input_text(text="", url=""):
    raw_text = (text or "").strip()
    raw_url = (url or "").strip()

    if raw_url:
        if not _looks_like_url(raw_url):
            raise InputValidationError("Invalid URL format. Use http:// or https://.")
        return _fetch_url_text(raw_url)

    if not raw_text:
        raise InputValidationError("Please provide text or URL.")

    if _looks_like_url(raw_text):
        return _fetch_url_text(raw_text)

    if len(raw_text) < 20:
        raise InputValidationError("Input text is too short. Provide at least 20 characters.")

    return raw_text


def predict_and_store(text="", url=""):
    resolved_text = _resolve_input_text(text=text, url=url)
    max_chars = int(current_app.config.get("MAX_INPUT_CHARS", 10000))
    resolved_text = resolved_text[:max_chars]

    predictor = get_predictor()
    result = predictor.predict(resolved_text)

    conn = get_db()
    insert_history_row(
        conn,
        text=resolved_text,
        prediction=result["prediction"],
        confidence=result["confidence"],
    )
    conn.commit()

    return {**result, "analyzed_text": resolved_text}


def get_history_records(limit=200):
    rows = fetch_history_rows(get_db(), limit=limit)
    return [dict(row) for row in rows]


def get_dashboard_data():
    data = fetch_dashboard_metrics(get_db())
    data["recent_activity"] = [dict(row) for row in data["recent_activity"]]
    return data
