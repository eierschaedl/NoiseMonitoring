import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

df = pd.read_csv('model_data/urbansound8k_features.csv')

# Separate features and labels
X = df.drop(columns=["clip_id", "label"])  # Drop non-numeric columns
y = df["label"]  # Extract labels

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save the scaler
joblib.dump(scaler, 'model_data/scaler.pkl')
print("Scaler saved as 'scaler.pkl'.")

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Save the label encoder
joblib.dump(label_encoder, 'model_data/label_encoder.pkl')
print("Label encoder saved as 'label_encoder.pkl'.")

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y_encoded)

X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, 'model_data/urbansound_model.pkl')
print("Model saved to 'urbansound_model.pkl'.")

# Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))