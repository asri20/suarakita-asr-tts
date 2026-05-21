"""
train_asr_cnn.py
Training ASR sederhana berbasis MFCC + CNN 1D

Struktur dataset:
asr/dataset/
├── ambil/
│   ├── ambil1.wav
│   └── ...
├── berhenti/
├── cepat/
└── ...

Output:
asr/model/model_asr.h5
asr/model/labels.json
asr/model/training_history.png
asr/model/confusion_matrix.png
"""

import os
import json
from pathlib import Path

import numpy as np
import librosa
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.utils import to_categorical


# ==============================
# KONFIGURASI
# ==============================

BASE_DIR = Path(__file__).resolve().parents[1]   # folder asr/
DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = BASE_DIR / "model"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 16000
DURATION = 2.0
N_MFCC = 13
MAX_LEN = 32

TEST_SIZE = 0.2
RANDOM_STATE = 42

EPOCHS = 150
BATCH_SIZE = 8


# ==============================
# PREPROCESSING AUDIO
# ==============================

def load_audio(file_path, sr=SAMPLE_RATE):
    audio, _ = librosa.load(file_path, sr=sr, mono=True)
    return audio


def normalize_audio(audio):
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val
    return audio


def trim_silence(audio, top_db=20):
    audio_trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
    return audio_trimmed


def pad_or_truncate(audio, sr=SAMPLE_RATE, duration=DURATION):
    target_len = int(sr * duration)

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


# ==============================
# EKSTRAKSI MFCC
# ==============================

def extract_mfcc(audio, sr=SAMPLE_RATE):
    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=N_MFCC
    )

    # Bentuk awal biasanya: (13, jumlah_frame)
    # Kita ubah agar panjang frame tetap MAX_LEN
    if mfcc.shape[1] < MAX_LEN:
        pad_width = MAX_LEN - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode="constant")
    else:
        mfcc = mfcc[:, :MAX_LEN]

    # CNN 1D butuh shape: (time_steps, features)
    # dari (13, 32) menjadi (32, 13)
    mfcc = mfcc.T

    return mfcc


# ==============================
# LOAD DATASET
# ==============================

def load_dataset():
    X = []
    y = []
    labels = []

    class_folders = sorted([
        folder for folder in DATASET_DIR.iterdir()
        if folder.is_dir()
    ])

    if not class_folders:
        raise ValueError(f"Tidak ada folder kelas di: {DATASET_DIR}")

    labels = [folder.name for folder in class_folders]

    print("Label ditemukan:")
    for idx, label in enumerate(labels):
        print(f"{idx}: {label}")

    for label_idx, class_folder in enumerate(class_folders):
        wav_files = sorted(class_folder.glob("*.wav"))

        print(f"\nMemproses kelas '{class_folder.name}' - {len(wav_files)} file")

        for wav_file in wav_files:
            try:
                audio = load_audio(wav_file)
                audio = preprocess_audio(audio)
                mfcc = extract_mfcc(audio)

                X.append(mfcc)
                y.append(label_idx)

            except Exception as e:
                print(f"Gagal memproses {wav_file}: {e}")

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int32)

    return X, y, labels


# ==============================
# MODEL CNN 1D
# ==============================

def build_model(input_shape, num_classes):
    model = Sequential([
        Conv1D(32, kernel_size=3, activation="relu", padding="same", input_shape=input_shape),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),

        Conv1D(64, kernel_size=3, activation="relu", padding="same"),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),

        Conv1D(128, kernel_size=3, activation="relu", padding="same"),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),

        Flatten(),

        Dense(128, activation="relu"),
        Dropout(0.2),

        Dense(64, activation="relu"),
        Dropout(0.2),

        Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# ==============================
# PLOT HASIL TRAINING
# ==============================

def plot_history(history):
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


def plot_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=(10, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(ax=ax, cmap="Blues", xticks_rotation=45)

    plt.title("Confusion Matrix")
    plt.tight_layout()

    output_path = MODEL_DIR / "confusion_matrix.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Confusion matrix disimpan: {output_path}")


# ==============================
# MAIN TRAINING
# ==============================

def main():
    print("Mulai load dataset...")
    X, y, labels = load_dataset()

    print("\nShape dataset:")
    print("X:", X.shape)
    print("y:", y.shape)
    print("Jumlah kelas:", len(labels))

    if len(X) == 0:
        raise ValueError("Dataset kosong. Pastikan file WAV ada di folder dataset.")

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

    print("\nData split:")
    print("Train:", X_train.shape)
    print("Test :", X_test.shape)

    input_shape = (MAX_LEN, N_MFCC)

    model = build_model(input_shape=input_shape, num_classes=num_classes)

    print("\nArsitektur model:")
    model.summary()

    model_path = MODEL_DIR / "model_asr.h5"

    callbacks = [
        ModelCheckpoint(
            filepath=str(model_path),
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1
        ),
        EarlyStopping(
            monitor="val_accuracy",
            patience=30,
            restore_best_weights=True,
            verbose=1
        )
    ]

    print("\nMulai training...")

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_test, y_test),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        verbose=1
    )

    print("\nEvaluasi model...")
    loss, acc = model.evaluate(X_test, y_test, verbose=0)

    print(f"Test Loss     : {loss:.4f}")
    print(f"Test Accuracy : {acc:.4f}")

    y_pred_prob = model.predict(X_test)
    y_pred = np.argmax(y_pred_prob, axis=1)

    print("\nClassification Report:")
    print(classification_report(y_test_raw, y_pred, target_names=labels))

    # Simpan model final
    model.save(model_path)
    print(f"\nModel disimpan ke: {model_path}")

    # Simpan labels
    labels_path = MODEL_DIR / "labels.json"
    with open(labels_path, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=4, ensure_ascii=False)

    print(f"Labels disimpan ke: {labels_path}")

    # Simpan grafik
    plot_history(history)
    plot_confusion_matrix(y_test_raw, y_pred, labels)

    print("\nTraining selesai.")


if __name__ == "__main__":
    main()