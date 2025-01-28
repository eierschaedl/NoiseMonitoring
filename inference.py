import joblib
import pandas as pd
import librosa
import numpy as np

# Load saved objects
model = joblib.load('model_data/urbansound_model.pkl')
scaler = joblib.load('model_data/scaler.pkl')
label_encoder = joblib.load('model_data/label_encoder.pkl')

def extract_features_from_file(file_path):
    """
    Extract features from an audio file path for inference.
    """
    y, sr = librosa.load(file_path, sr=16000)
    n_fft = 512

    if len(y) < n_fft:
        y = np.pad(y, (0, n_fft - len(y)), mode="constant")

    # Extract features
    features = {
        "spectral_centroid": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=n_fft)),
        "spectral_bandwidth": np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr, n_fft=n_fft)),
        "spectral_contrast": np.mean(librosa.feature.spectral_contrast(y=y, sr=sr, n_fft=n_fft)),
        "mfccs_mean": list(np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)),
        "cqt_mean": list(np.mean(librosa.feature.chroma_cqt(y=y, sr=sr), axis=1)),
    }
    return features

def predict_single(file_path):
    """
    Predict the label for a single audio file.
    """
    # Extract features
    features = extract_features_from_file(file_path)

    # Flatten feature dictionary
    feature_vector = pd.DataFrame([{
        "spectral_centroid": features["spectral_centroid"],
        "spectral_bandwidth": features["spectral_bandwidth"],
        "spectral_contrast": features["spectral_contrast"],
        **{f"mfcc_{i+1}": mfcc_val for i, mfcc_val in enumerate(features["mfccs_mean"])},
        **{f"cqt_{i+1}": cqt_val for i, cqt_val in enumerate(features["cqt_mean"])},
    }])

    # Normalize using the scaler
    feature_vector_scaled = scaler.transform(feature_vector)

    # Make analysis
    prediction_encoded = model.predict(feature_vector_scaled)

    # Decode the label
    prediction_label = label_encoder.inverse_transform(prediction_encoded)
    return prediction_label[0]

# Example usage
if __name__ == "__main__":
    file_path = "testfiles/siren.wav"
    predicted_label = predict_single(file_path)
    print(f"Predicted label: {predicted_label}")
