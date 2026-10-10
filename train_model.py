import os
import time

import mlflow
import mlflow.sklearn
import numpy as np
from mlflow.models import infer_signature
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(tracking_uri)

for attempt in range(30):
    try:
        mlflow.set_experiment("college-erp-student-performance")
        break
    except Exception:
        if attempt == 29:
            raise
        time.sleep(2)

rng = np.random.default_rng(42)
attendance = rng.uniform(45, 100, size=300)
study_hours = rng.uniform(0, 30, size=300)
absences = rng.integers(0, 21, size=300)
features = np.column_stack([attendance, study_hours, absences])
labels = 15 + 0.45 * attendance + 1.2 * study_hours - 1.1 * absences + rng.normal(0, 3, size=300)
train_x, test_x, train_y, test_y = train_test_split(features, labels, test_size=0.2, random_state=42)

with mlflow.start_run(run_name="linear-regression-baseline"):
    mlflow.log_params({"model": "LinearRegression", "test_size": 0.2, "random_state": 42})
    model = LinearRegression().fit(train_x, train_y)
    predictions = model.predict(test_x)
    mlflow.log_metric("mae_score", mean_absolute_error(test_y, predictions))
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="StudentPerformancePredictor",
        signature=infer_signature(train_x, model.predict(train_x)),
        input_example=[[85, 12, 2]],
    )
    print("Trained, tracked, and registered StudentPerformancePredictor model.")
