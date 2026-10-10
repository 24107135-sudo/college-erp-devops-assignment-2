import os

import mlflow
import mlflow.pyfunc
from flask import Flask, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
REQUESTS = Counter("college_erp_predictions_total", "Student score prediction requests", ["result"])
LATENCY = Histogram("college_erp_prediction_seconds", "Student score prediction endpoint latency")
MODEL = None


def load_model():
    global MODEL
    if MODEL is None:
        MODEL = mlflow.pyfunc.load_model("models:/StudentPerformancePredictor/1")
    return MODEL


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.post("/predict")
@LATENCY.time()
def predict():
    values = request.get_json(silent=True)
    if not isinstance(values, dict):
        REQUESTS.labels(result="invalid").inc()
        return jsonify(error="Send JSON with attendance_percent, study_hours_week and absences"), 400
    try:
        attendance = float(values["attendance_percent"])
        study_hours = float(values["study_hours_week"])
        absences = float(values["absences"])
        if not 0 <= attendance <= 100 or not 0 <= study_hours <= 40 or not 0 <= absences <= 60:
            raise ValueError
        prediction = float(load_model().predict([[attendance, study_hours, absences]])[0])
    except (KeyError, TypeError, ValueError):
        REQUESTS.labels(result="invalid").inc()
        return jsonify(error="attendance_percent must be 0-100, study_hours_week 0-40 and absences 0-60"), 400
    REQUESTS.labels(result="success").inc()
    return jsonify(predicted_score=round(min(100, max(0, prediction)), 1))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
