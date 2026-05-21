"""
preprocess.py - Modul preprocessing audio untuk ASR
Handles audio loading, normalization, and preparation
"""

import numpy as np
import librosa
import soundfile as sf
import os


# Konfigurasi audio
SAMPLE_RATE = 16000
DURATION = 2.0          # detik
N_MFCC = 13
MAX_LEN = 32            # frames MFCC

# BARU (10 robot commands):
LABELS = [
    "ambil", "berhenti", "cepat", "kanan", "kiri", 
    "lambat", "lepas", "maju", "mulai", "mundur"
]


def load_audio(file_path: str, sr: int = SAMPLE_RATE) -> np.ndarray:
    """Load file audio dan resample ke sample rate target."""
    try:
        audio, _ = librosa.load(file_path, sr=sr, mono=True)
        return audio
    except Exception as e:
        raise ValueError(f"Gagal memuat audio dari {file_path}: {e}")


def load_audio_from_bytes(audio_bytes: bytes, sr: int = SAMPLE_RATE) -> np.ndarray:
    """Load audio dari bytes (upload Streamlit)."""
    import io
    try:
        audio, _ = librosa.load(io.BytesIO(audio_bytes), sr=sr, mono=True)
        return audio
    except Exception as e:
        raise ValueError(f"Gagal memuat audio dari bytes: {e}")


def normalize_audio(audio: np.ndarray) -> np.ndarray:
    """Normalisasi amplitude audio ke range [-1, 1]."""
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val
    return audio


def trim_silence(audio: np.ndarray, sr: int = SAMPLE_RATE,
                 top_db: int = 20) -> np.ndarray:
    """Hapus silence di awal dan akhir audio."""
    audio_trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
    return audio_trimmed


def pad_or_truncate(audio: np.ndarray, sr: int = SAMPLE_RATE,
                    duration: float = DURATION) -> np.ndarray:
    """Padding atau truncate audio ke durasi tetap."""
    target_len = int(sr * duration)
    if len(audio) < target_len:
        # Pad dengan zeros
        audio = np.pad(audio, (0, target_len - len(audio)), mode='constant')
    else:
        # Truncate
        audio = audio[:target_len]
    return audio


def preprocess_audio(audio: np.ndarray, sr: int = SAMPLE_RATE) -> np.ndarray:
    """Pipeline preprocessing lengkap."""
    audio = normalize_audio(audio)
    audio = trim_silence(audio, sr=sr)
    audio = pad_or_truncate(audio, sr=sr)
    return audio


def preprocess_file(file_path: str) -> np.ndarray:
    """Load dan preprocess file audio."""
    audio = load_audio(file_path)
    return preprocess_audio(audio)


def preprocess_bytes(audio_bytes: bytes) -> np.ndarray:
    """Load dan preprocess audio dari bytes."""
    audio = load_audio_from_bytes(audio_bytes)
    return preprocess_audio(audio)


def get_label_index(label: str) -> int:
    """Dapatkan index label dari nama."""
    if label in LABELS:
        return LABELS.index(label)
    raise ValueError(f"Label '{label}' tidak dikenal. Label valid: {LABELS}")


def get_label_from_index(index: int) -> str:
    """Dapatkan nama label dari index."""
    if 0 <= index < len(LABELS):
        return LABELS[index]
    raise ValueError(f"Index {index} di luar range 0-{len(LABELS)-1}")
