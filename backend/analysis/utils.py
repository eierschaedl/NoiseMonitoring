import joblib
import pandas as pd
import librosa
import numpy as np
import os

MODEL_DATA_PATH = os.path.join(os.path.dirname(__file__), 'model_data')

def load_model():
    model_path = os.path.join(MODEL_DATA_PATH, 'urbansound_model.pkl')
    return joblib.load(model_path)

def load_scaler():
    scaler_path = os.path.join(MODEL_DATA_PATH, 'scaler.pkl')
    return joblib.load(scaler_path)

def load_label_encoder():
    encoder_path = os.path.join(MODEL_DATA_PATH, 'label_encoder.pkl')
    return joblib.load(encoder_path)

def extract_features_from_file(file):
    y, sr = librosa.load(file, sr=16000)
    n_fft = 512

    if len(y) < n_fft:
        y = np.pad(y, (0, n_fft - len(y)), mode="constant")

    features = {
        "spectral_centroid": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=n_fft)),
        "spectral_bandwidth": np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr, n_fft=n_fft)),
        "spectral_contrast": np.mean(librosa.feature.spectral_contrast(y=y, sr=sr, n_fft=n_fft)),
        "mfccs_mean": list(np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)),
        "cqt_mean": list(np.mean(librosa.feature.chroma_cqt(y=y, sr=sr), axis=1)),
    }

    return features

def predict(file_path):

    features = extract_features_from_file(file_path)

    feature_vector = pd.DataFrame([{
        "spectral_centroid": features["spectral_centroid"],
        "spectral_bandwidth": features["spectral_bandwidth"],
        "spectral_contrast": features["spectral_contrast"],
        **{f"mfcc_{i+1}": val for i, val in enumerate(features["mfccs_mean"])},
        **{f"cqt_{i+1}": val for i, val in enumerate(features["cqt_mean"])},
    }])

    model = load_model()
    scaler = load_scaler()
    label_encoder = load_label_encoder()

    feature_vector_scaled = scaler.transform(feature_vector)
    prediction_encoded = model.predict(feature_vector_scaled)
    prediction_label = label_encoder.inverse_transform(prediction_encoded)

    return prediction_label[0]

def analyze(file_path):
    prediction = predict(file_path)

    db = measure_volume(file_path)

    response = "Lautstärke überschreitet keine Grenzwerte."

    if db > 45:
        response = "Gesundheitliche Risiken: "
        response += add_health_to_response(db)
        if prediction == 'drilling' or prediction == 'jackhammer':
            response += "\nBaulärm: " + add_construction_to_response(db)
        if db > 50:
            response += "\nArbeitslärm: " + add_work_to_response(db)
            if prediction == 'car_horn' or prediction == 'engine_idling':
                response += "\nVerkehrslärm: " + add_traffic_to_response(db)

    return response

def measure_volume(file_path):
    # Load the audio file using librosa
    y, sr = librosa.load(file_path, sr=None)  # Load with original sample rate

    # Calculate the RMS (Root Mean Square) energy of the signal
    rms = librosa.feature.rms(y=y)

    # Calculate the average RMS value across the entire audio
    rms_mean = np.mean(rms)

    # Convert the RMS value to decibels
    db = 20 * np.log10(rms_mean) if rms_mean > 0 else -np.inf  # Avoid log(0) by returning -inf if RMS is 0

    # Convert dBFS to dB using reference level 94 dB
    db += 94

    return db

def add_health_to_response(db):
    if db > 75:
        return "Warnung: Risiko eines dauerhaften Gehörverlusts bei längerer Exposition. Tragen Sie einen Gehörschutz oder reduzieren Sie den Lärmpegel."
    elif db > 65:
        return "Achtung! Gesundheitliche Schäden durch Lärmbelastung möglich. Tragen Sie einen Gehörschutz oder reduzieren Sie den Lärmpegel."
    elif db > 55:
        return "Starke Schlafstörungen und Beeinträchtigung der Konzentration. Reduzieren Sie den Lärm, um gesundheitliche Risiken zu vermeiden."
    else:
        return "Leichte Schlafstörungen möglich. Minimieren Sie Lärmquellen in der Umgebung, um erholsamen Schlaf zu gewährleisten."

def add_construction_to_response(db):
    if db > 55:
        return "Baulärm überschreitet den Grenzwert. Bitte besprechen Sie das mit der Bauleitung oder wenden Sie sich ggf an die zuständigen Behörden."
    else:
        return "Nachtlärmgrenzwert für Bautätigkeiten überschritten. Bitte besprechen Sie das mit der Bauleitung oder wenden Sie sich ggf an die zuständigen Behörden."

def add_traffic_to_response(db):
    if db > 60:
        return "Verkehrslärmgrenzwert überschritten. Bitte informieren Sie sich über mögliche bauliche Lärmschutzmaßnahmen oder wenden Sie sich ggf an die zuständigen Behörden."
    else:
        return "Nachtlärmgrenzwert für Verkehr überschritten. Bitte informieren Sie sich über mögliche bauliche Lärmschutzmaßnahmen oder wenden Sie sich ggf an die zuständigen Behörden."

def add_work_to_response(db):
    if db > 85:
        return "Achtung! Expositionsgrenzwert überschritten. Maßnahmen zur sofortigen Reduktion des Lärms sind notwendig."
    elif db > 80:
        return "Bitte arbeiten Sie nur noch mit Gehörschutz! Ihr Arbeitgeber ist verpflichtet diesen bereitzustellen."
    elif db > 65:
        return "Lärmpegel für Bürotätigkeiten überschritten. Reduzieren Sie mögliche Lärmquellen oder besprechen Sie das mit Ihrem Arbeitgeber."
    else:
        return "Konzentration bei geistiger Arbeit beeinträchtigt. Reduzieren Sie mögliche Lärmquellen oder besprechen Sie das mit Ihrem Arbeitgeber."