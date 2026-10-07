import numpy as np
import joblib
from tensorflow.keras.models import load_model

# ==============================
# LOAD MODELS (LOAD ONLY ONCE)
# ==============================

xgb_model = joblib.load("model/xgb_model.pkl")
lgbm_model = joblib.load("model/lgbm_model.pkl")
scaler = joblib.load("model/scaler.pkl")
cnn_lstm_model = load_model("model/cnn_lstm_model.h5")

# ==============================
# CLASS LABELS
# ==============================

class_names = [
    "Seizure",
    "Tumor",
    "Healthy",
    "Eyes Closed",
    "Eyes Open"
]

# ==============================
# PREDICTION FUNCTION
# ==============================

def run_prediction(values):

    input_array = np.array(values).reshape(1, -1)

    # Validate feature length
    if input_array.shape[1] != 178:
        raise ValueError(f"Expected 178 features but got {input_array.shape[1]}")

    # Scale input
    input_scaled = scaler.transform(input_array)

    # ==============================
    # ENSEMBLE PREDICTION
    # ==============================

    proba_xgb = xgb_model.predict_proba(input_scaled)
    proba_lgbm = lgbm_model.predict_proba(input_scaled)

    avg_proba = (proba_xgb + proba_lgbm) / 2

    ensemble_pred = np.argmax(avg_proba, axis=1)

    ensemble_label = class_names[ensemble_pred[0]]

    # ==============================
    # CNN + LSTM PREDICTION
    # ==============================

    input_dl = input_scaled.reshape(1, input_scaled.shape[1], 1)

    cnn_pred_prob = cnn_lstm_model.predict(input_dl)

    cnn_pred = np.argmax(cnn_pred_prob, axis=1)

    cnn_label = class_names[cnn_pred[0]]

    return {
        "ensemble_prediction": ensemble_label,
        "cnn_lstm_prediction": cnn_label
    }