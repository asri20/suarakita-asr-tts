"""
utils.py - Utility functions untuk modul ASR
"""

import os
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
from typing import Tuple, List, Optional

from .preprocess import LABELS, SAMPLE_RATE, N_MFCC, MAX_LEN
from .feature_extraction import extract_mfcc


def load_dataset(dataset_dir: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load seluruh dataset dari folder struktur:
    dataset/
      ├── yesus/  (berisi file .wav)
      ├── simon/
      └── ...
    
    Returns:
        X: array features shape (n_samples, MAX_LEN, N_MFCC)
        y: array labels (integer encoded)
    """
    from .preprocess import preprocess_audio, load_audio

    X, y = [], []
    dataset_path = Path(dataset_dir)

    print(f"[INFO] Memuat dataset dari: {dataset_path}")

    for label_idx, label_name in enumerate(LABELS):
        label_dir = dataset_path / label_name
        if not label_dir.exists():
            print(f"[WARN] Folder tidak ditemukan: {label_dir}")
            continue

        wav_files = list(label_dir.glob("*.wav")) + list(label_dir.glob("*.WAV"))
        print(f"  [{label_name}] → {len(wav_files)} file audio")

        for wav_file in wav_files:
            try:
                audio = load_audio(str(wav_file))
                audio = preprocess_audio(audio)
                mfcc = extract_mfcc(audio)
                X.append(mfcc)
                y.append(label_idx)
            except Exception as e:
                print(f"  [ERROR] Gagal proses {wav_file.name}: {e}")

    if not X:
        raise ValueError("Dataset kosong! Pastikan folder dataset berisi file .wav")

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int32)
    print(f"\n[INFO] Dataset berhasil dimuat: {X.shape[0]} sampel")
    print(f"[INFO] Shape X: {X.shape}, Shape y: {y.shape}")
    return X, y


def get_dataset_stats(dataset_dir: str) -> dict:
    """Hitung statistik dataset per kelas."""
    dataset_path = Path(dataset_dir)
    stats = {}
    total = 0
    for label_name in LABELS:
        label_dir = dataset_path / label_name
        if label_dir.exists():
            count = len(list(label_dir.glob("*.wav")) + list(label_dir.glob("*.WAV")))
            stats[label_name] = count
            total += count
        else:
            stats[label_name] = 0
    stats['_total'] = total
    return stats


def save_audio(audio: np.ndarray, file_path: str, sr: int = SAMPLE_RATE) -> None:
    """Simpan array audio ke file WAV."""
    sf.write(file_path, audio, sr)


def audio_duration(audio: np.ndarray, sr: int = SAMPLE_RATE) -> float:
    """Hitung durasi audio dalam detik."""
    return len(audio) / sr


def top_k_predictions(probs: np.ndarray, k: int = 3) -> List[Tuple[str, float]]:
    """
    Dapatkan top-k prediksi beserta confidence score.
    
    Returns:
        List of (label_name, probability) diurutkan descending
    """
    sorted_idx = np.argsort(probs)[::-1][:k]
    return [(LABELS[i], float(probs[i])) for i in sorted_idx]


def model_summary_text(model) -> str:
    """Dapatkan ringkasan model sebagai string."""
    lines = []
    model.summary(print_fn=lambda x: lines.append(x))
    return '\n'.join(lines)
