"""
train_asr_cnn_v2.py
Training ASR Command Recognition
Versi lebih ringan untuk dataset kecil-menengah.

Output:
- asr/model/model_asr.h5
- asr/model/labels.json
- asr/model/training_history.png
- asr/model/confusion_matrix.png
"""

import json
from pathlib import Path

import librosa
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical


# =========================
# KONFIGURASI
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]  # folder asr/
DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = BASE_DIR / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 16000
DURATION = 2.0
N_MFCC = 13
MAX_LEN = 32
TOP_DB = 30

TEST_SIZE = 0.1
RANDOM_STATE = 42

EPOCHS = 250
BATCH_SIZE = 8


# =========================
# PREPROCESSING
# =========================

def load_audio(file_path):
    audio, _ = librosa.load(file_path, sr=SAMPLE_RATE, mono=True)
    return audio


def normalize_audio(audio):
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val
    return audio


def trim_silence(audio):
    """
    top_db=30 dibuat lebih longgar daripada 20.
    Tujuannya supaya awal/akhir kata tidak terlalu mudah kepotong.
    """
    audio_trimmed, _ = librosa.effects.trim(audio, top_db=TOP_DB)

    # Kalau hasil trim terlalu pendek, pakai audio asli
    if len(audio_trimmed) < int(0.3 * SAMPLE_RATE):
        return audio

    return audio_trimmed


def pad_or_truncate(audio):
    target_len = int(SAMPLE_RATE * DURATION)

    if len(audio) < target_len:
        audio = np.pad(audio, (0, target_len - len(audio)), mode="constant")
    else:
        audio = audio[:target_len]

    return audio


def preprocess_audio(audio):
    audio = normalize_audio(audio)
    audio = trim_silence(audio)
    audio = pad_or_truncate(audio)
    return audio


# =========================
# MFCC
# =========================

def extract_mfcc(audio):
    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=SAMPLE_RATE,
        n_mfcc=N_MFCC
    )

    if mfcc.shape[1] < MAX_LEN:
        pad_width = MAX_LEN - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode="constant")
    else:
        mfcc = mfcc[:, :MAX_LEN]

    # dari (13, 32) jadi (32, 13)
    mfcc = mfcc.T

    return mfcc


# =========================
# LOAD DATASET
# =========================

def load_dataset():
    X = []
    y = []

    class_folders = sorted([
        folder for folder in DATASET_DIR.iterdir()
        if folder.is_dir()
    ])

    labels = [folder.name for folder in class_folders]

    print("\nLabel yang ditemukan:")
    for idx, label in enumerate(labels):
        print(f"{idx}: {label}")

    print("\nJumlah file per kelas:")

    for label_idx, class_folder in enumerate(class_folders):
        wav_files = sorted(class_folder.glob("*.wav"))
        print(f"{class_folder.name}: {len(wav_files)} file")

        for wav_file in wav_files:
            try:
                audio = load_audio(wav_file)
                audio = preprocess_audio(audio)
                mfcc = extract_mfcc(audio)

                X.append(mfcc)
                y.append(label_idx)

            except Exception as e:
                print(f"Gagal proses {wav_file}: {e}")

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int32)

    return X, y, labels


# =========================
# MODEL CNN KECIL
# =========================

def build_model(input_shape, num_classes):
    model = Sequential([
        Conv1D(
            filters=32,
            kernel_size=3,
            activation="relu",
            padding="same",
            input_shape=input_shape
        ),
        MaxPooling1D(pool_size=2),

        Conv1D(
            filters=64,
            kernel_size=3,
            activation="relu",
            padding="same"
        ),
        MaxPooling1D(pool_size=2),

        Flatten(),

        Dense(64, activation="relu"),
        Dropout(0.1),

        Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# =========================
# PLOT
# =========================

def save_training_plot(history):
    plt.figure(figsize=(10, 4))

    plt.plot(history.history["accuracy"], label="Train Accuracy")
    plt.plot(history.history["val_accuracy"], label="Validation Accuracy")

    plt.title("Training Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)

    output_path = MODEL_DIR / "training_history.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Grafik training disimpan: {output_path}")


def save_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=(10, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(ax=ax, xticks_rotation=45)

    plt.title("Confusion Matrix")
    plt.tight_layout()

    output_path = MODEL_DIR / "confusion_matrix.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Confusion matrix disimpan: {output_path}")


# =========================
# MAIN
# =========================

def main():
    print("Mulai load dataset...")

    X, y, labels = load_dataset()

    print("\nShape data:")
    print("X:", X.shape)
    print("y:", y.shape)
    print("Jumlah kelas:", len(labels))

    if len(X) == 0:
        raise ValueError("Dataset kosong. Cek folder asr/dataset.")

    num_classes = len(labels)
    y_cat = to_categorical(y, num_classes=num_classes)

    X_train, X_test, y_train, y_test, y_train_raw, y_test_raw = train_test_split(
        X,
        y_cat,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    print("\nSplit dataset:")
    print("Train:", X_train.shape)
    print("Test :", X_test.shape)

    input_shape = (MAX_LEN, N_MFCC)

    model = build_model(input_shape, num_classes)

    print("\nArsitektur model:")
    model.summary()

    print("\nMulai training...")

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_test, y_test),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=1,
        shuffle=True
    )

    print("\nEvaluasi...")
    loss, acc = model.evaluate(X_test, y_test, verbose=0)

    print(f"Test Loss     : {loss:.4f}")
    print(f"Test Accuracy : {acc:.4f}")

    y_pred_prob = model.predict(X_test)
    y_pred = np.argmax(y_pred_prob, axis=1)

    print("\nClassification Report:")
    print(classification_report(y_test_raw, y_pred, target_names=labels))

    model_path = MODEL_DIR / "model_asr.h5"
    model.save(model_path)

    labels_path = MODEL_DIR / "labels.json"
    with open(labels_path, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=4, ensure_ascii=False)

    save_training_plot(history)
    save_confusion_matrix(y_test_raw, y_pred, labels)

    print("\nTraining selesai.")
    print(f"Model disimpan ke : {model_path}")
    print(f"Labels disimpan ke: {labels_path}")


if __name__ == "__main__":
    main()