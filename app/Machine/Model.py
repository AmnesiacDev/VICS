import os
import pickle
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


class VoiceCommandModel:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = None
        self.label_encoder = LabelEncoder()
        self.X = []
        self.y = []

    def extract_features(self, file_path):
        try:
            audio, sr = librosa.load(file_path, sr=None)
            mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
            mfcc_scaled = np.mean(mfcc.T, axis=0)
            return mfcc_scaled
        except Exception as e:
            print(f" Failed to extract features from {file_path}: {e}")
            return None

    def process_audio_files(self):
        print(" Extracting features from dataset...")
        for command_dir in os.listdir(self.data_path):
            full_command_path = os.path.join(self.data_path, command_dir)
            if not os.path.isdir(full_command_path):
                continue
            for file in os.listdir(full_command_path):
                if file.endswith(".wav"):
                    file_path = os.path.join(full_command_path, file)
                    features = self.extract_features(file_path)
                    if features is not None:
                        self.X.append(features)
                        self.y.append(command_dir)

        self.X = np.array(self.X)
        self.y = self.label_encoder.fit_transform(self.y)
        print(f" Processed {len(self.X)} samples from {len(set(self.y))} classes.")

    def train_model(self, model_type='svm'):
        if len(self.X) == 0 or len(self.y) == 0:
            print(" No data to train on.")
            return

        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )

        if model_type == 'svm':
            self.model = SVC(kernel='linear', probability=True)
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100)
        elif model_type == 'mlp':
            self.model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=300)
        else:
            raise ValueError("Invalid model type. Choose 'svm', 'random_forest', or 'mlp'.")

        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        print(f"{model_type.upper()} Accuracy: {acc * 100:.2f}%")

    def save_model(self, file_path):
        if self.model is None:
            print(" Model is None, cannot save.")
            return

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, 'wb') as f:
                pickle.dump({
                    'model': self.model,
                    'label_encoder': self.label_encoder
                }, f)
            print(f"Model saved successfully at: {os.path.abspath(file_path)}")
        except Exception as e:
            print(f" Failed to save model: {e}")

    def load_model(self, file_path="model.pkl"):
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.label_encoder = data['label_encoder']
            print(" Model loaded successfully.")
        except Exception as e:
            print(f" Failed to load model: {e}")

    def predict_command(self, file_path):
        features = self.extract_features(file_path)
        if features is None:
            raise ValueError("Could not extract features for prediction.")
        prediction = self.model.predict([features])[0]
        confidence = np.max(self.model.predict_proba([features]))
        command = self.label_encoder.inverse_transform([prediction])[0]
        return command, confidence
