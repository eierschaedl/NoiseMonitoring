import librosa
import numpy as np
import pandas as pd
import soundata

# Initialize and validate the UrbanSound8K dataset
dataset = soundata.initialize('urbansound8k')
#dataset.download()
dataset.validate()

def extract_features(clip):
    """
    Extract features from a soundata Clip object.
    """
    file_path = clip.audio_path
    y, sr = librosa.load(file_path, sr=16000)

    # Dynamically adjust n_fft based on signal length (padding short signals)
    n_fft = 512  # Fixed n_fft value

    # Pad the signal if it's shorter than the required length (512)
    if len(y) < n_fft:
        y = np.pad(y, (0, n_fft - len(y)), mode="constant")

    # Print to check the signal length and n_fft for debugging´
    print(f"Clip {clip.clip_id}: Signal length = {len(y)}, n_fft = {n_fft}")

    # Extract features
    features = {
        "spectral_centroid": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=n_fft)),
        "spectral_bandwidth": np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr, n_fft=n_fft)),
        "spectral_contrast": np.mean(librosa.feature.spectral_contrast(y=y, sr=sr, n_fft=n_fft)),
        "mfccs_mean": list(np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)),
        "cqt_mean": list(np.mean(librosa.feature.chroma_cqt(y=y, sr=sr), axis=1)),
    }
    return features

# Helper function to handle tags
def get_primary_label(clip):
    """
    Retrieve the primary label from clip tags.
    """
    if hasattr(clip.tags, 'labels') and clip.tags.labels:
        return clip.tags.labels[0]  # First label if available
    return "unknown"  # Default to "unknown" if no label exists

# Process all clips in the dataset
data = []
for clip_id in dataset.clip_ids:  # Iterate over clip IDs
    clip = dataset.clip(clip_id)  # Retrieve the Clip object for each ID
    try:
        # Extract features
        features = extract_features(clip)
        # Handle tags dynamically
        label = get_primary_label(clip)
        # Flatten the feature dictionary for storage
        row = {
            "clip_id": clip.clip_id,  # Unique identifier for each clip
            "label": label,           # Primary label for the clip
            "spectral_centroid": features["spectral_centroid"],
            "spectral_bandwidth": features["spectral_bandwidth"],
            "spectral_contrast": features["spectral_contrast"],
        }
        # Add MFCCs and CQT features as separate columns
        for i, mfcc_val in enumerate(features["mfccs_mean"]):
            row[f"mfcc_{i+1}"] = mfcc_val
        for i, cqt_val in enumerate(features["cqt_mean"]):
            row[f"cqt_{i+1}"] = cqt_val
        # Append the row to the dataset
        data.append(row)
    except Exception as e:
        print(f"Error processing clip {clip_id}: {e}")

# Convert the dataset to a Pandas DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("urbansound8k_features.csv", index=False)
print("Feature extraction complete. Data saved to 'urbansound8k_features.csv'.")