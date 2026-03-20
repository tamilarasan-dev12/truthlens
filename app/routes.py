from flask import (
    Blueprint,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from app.services import (
    ExternalContentError,
    InputValidationError,
    get_history_records,
    predict_and_store,
)

bp = Blueprint("main", __name__)


def api_success(data):
    return jsonify({"status": "success", "data": data, "error": None}), 200


def api_error(message, status_code):
    return jsonify({"status": "error", "data": None, "error": message}), status_code


@bp.route("/")
def index():
    return redirect(url_for("main.analyze"))


@bp.route("/analyze", methods=["GET", "POST"])
def analyze():
    result = None
    error_message = None
    form_data = {"text_input": "", "url_input": ""}

    if request.method == "POST":
        form_data["text_input"] = request.form.get("text_input", "").strip()
        form_data["url_input"] = request.form.get("url_input", "").strip()
        try:
            result = predict_and_store(
                text=form_data["text_input"],
                url=form_data["url_input"],
            )
        except (InputValidationError, ExternalContentError) as exc:
            error_message = str(exc)
        except Exception:
            current_app.logger.exception("Unexpected failure in /analyze")
            error_message = "Unexpected server error. Please try again."

    return render_template(
        "analyze.html",
        result=result,
        error_message=error_message,
        form_data=form_data,
    )


@bp.route("/history")
def history():
    records = get_history_records(limit=500)
    return render_template("history.html", records=records)


@bp.route("/api/v1/predict", methods=["POST"])
def api_predict():
    payload = request.get_json(silent=True)
    if payload is None:
        return api_error("Request body must be valid JSON.", 400)

    text = str(payload.get("text", "")).strip()
    url = str(payload.get("url", "")).strip()
    if not text and not url:
        return api_error("Please provide text or URL.", 400)

    try:
        result = predict_and_store(text=text, url=url)
        return api_success(result)
    except InputValidationError as exc:
        return api_error(str(exc), 400)
    except ExternalContentError as exc:
        return api_error(str(exc), 422)
    except Exception:
        current_app.logger.exception("Unexpected failure in API")
        return api_error("Unexpected server error.", 500)