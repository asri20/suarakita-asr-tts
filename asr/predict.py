"""
predict.py - Inferensi model ASR untuk prediksi nama
Mendukung input: file path, bytes (upload), atau array numpy
"""

import numpy as np
import os
from pathlib import Path
from typing import Union, Optional, Tuple, List

from .preprocess import LABELS, N_MFCC, MAX_LEN, preprocess_audio, preprocess_bytes
from .feature_extraction import extract_mfcc
from .utils import top_k_predictions


# ── Singleton model loader ─────────────────────────────────────────────────────
_model = None
_model_path = Path(__file__).parent / "model" / "model_asr.h5"


def load_model(model_path: Optional[str] = None):
    """Load model TensorFlow/Keras dari file .h5"""
    global _model

    if _model is not None:
        return _model

    import tensorflow as tf

    path = Path(model_path) if model_path else _model_path

    if not path.exists():
        raise FileNotFoundError(
            f"Model tidak ditemukan di: {path}\n"
            "Jalankan training di Google Colab terlebih dahulu, "
            "lalu letakkan model_asr.h5 di folder asr/model/"
        )

    _model = tf.keras.models.load_model(str(path))
    print(f"[ASR] Model berhasil dimuat dari: {path}")
    return _model


def is_model_available(model_path: Optional[str] = None) -> bool:
    """Periksa apakah model sudah tersedia."""
    path = Path(model_path) if model_path else _model_path
    return path.exists()


def predict_from_audio(audio: np.ndarray, model=None) -> dict:
    """
    Prediksi nama dari array audio yang sudah dipreprocess.
    
    Args:
        audio: sinyal audio numpy array (sudah preprocessed)
        model: model keras (opsional, auto-load jika None)
    
    Returns:
        dict dengan keys: label, confidence, probabilities, top_k
    """
    if model is None:
        model = load_model()

    # Ekstrak MFCC
    mfcc = extract_mfcc(audio)              # (MAX_LEN, N_MFCC)
    mfcc_input = mfcc[np.newaxis, ...]      # (1, MAX_LEN, N_MFCC)

    # Prediksi
    probs = model.predict(mfcc_input, verbose=0)[0]   # (num_classes,)

    pred_idx = int(np.argmax(probs))
    pred_label = LABELS[pred_idx]
    confidence = float(probs[pred_idx])
    top_k = top_k_predictions(probs, k=5)

    return {
        "label": pred_label,
        "label_capitalized": pred_label.capitalize(),
        "confidence": confidence,
        "confidence_pct": confidence * 100,
        "probabilities": probs,
        "top_k": top_k,
        "mfcc": mfcc,
        "audio": audio,
    }


def predict_from_bytes(audio_bytes: bytes, model=None) -> dict:
    """Prediksi dari bytes audio (upload Streamlit)."""
    audio = preprocess_bytes(audio_bytes)
    return predict_from_audio(audio, model=model)


def predict_from_file(file_path: str, model=None) -> dict:
    """Prediksi dari file audio."""
    from .preprocess import load_audio
    audio = load_audio(file_path)
    audio = preprocess_audio(audio)
    return predict_from_audio(audio, model=model)


def create_demo_model():
    """
    Buat model demo ringan untuk keperluan preview UI
    tanpa dataset asli. Model ini TIDAK akurat — hanya untuk demo tampilan.
    """
    import tensorflow as tf

    num_classes = len(LABELS)
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(MAX_LEN, N_MFCC)),
        tf.keras.layers.Conv1D(32, 3, activation='relu', padding='same'),
        tf.keras.layers.MaxPooling1D(2),
        tf.keras.layers.Conv1D(64, 3, activation='relu', padding='same'),
        tf.keras.layers.MaxPooling1D(2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(num_classes, activation='softmax'),
    ], name="ASR_CNN1D_Demo")

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


def predict_demo(audio: np.ndarray) -> dict:
    """
    Prediksi demo menggunakan model random (tanpa training).
    Digunakan saat model_asr.h5 belum tersedia.
    """
    model = create_demo_model()
    mfcc = extract_mfcc(audio)
    mfcc_input = mfcc[np.newaxis, ...]
    probs = model.predict(mfcc_input, verbose=0)[0]

    pred_idx = int(np.argmax(probs))
    pred_label = LABELS[pred_idx]
    confidence = float(probs[pred_idx])
    top_k = top_k_predictions(probs, k=5)

    return {
        "label": pred_label,
        "label_capitalized": pred_label.capitalize(),
        "confidence": confidence,
        "confidence_pct": confidence * 100,
        "probabilities": probs,
        "top_k": top_k,
        "mfcc": mfcc,
        "audio": audio,
        "is_demo": True,
    }
