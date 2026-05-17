"""
ASR Module - Automatic Speech Recognition Bahasa Indonesia
Menggunakan MFCC + CNN1D model berbasis TensorFlow/Keras
"""

from .preprocess import (
    LABELS, SAMPLE_RATE, N_MFCC, MAX_LEN,
    load_audio, load_audio_from_bytes,
    preprocess_audio, preprocess_bytes, preprocess_file,
    normalize_audio, trim_silence, pad_or_truncate,
)

from .feature_extraction import (
    extract_mfcc, extract_mfcc_from_file, extract_mfcc_from_bytes,
    plot_mfcc, plot_confidence,
)

from .predict import (
    load_model, is_model_available,
    predict_from_audio, predict_from_bytes, predict_from_file,
    predict_demo, create_demo_model,
)

from .utils import (
    load_dataset, get_dataset_stats,
    save_audio, audio_duration, top_k_predictions,
)

__all__ = [
    "LABELS", "SAMPLE_RATE", "N_MFCC", "MAX_LEN",
    "load_audio", "load_audio_from_bytes",
    "preprocess_audio", "preprocess_bytes", "preprocess_file",
    "extract_mfcc", "plot_mfcc", "plot_confidence",
    "load_model", "is_model_available",
    "predict_from_audio", "predict_from_bytes", "predict_from_file",
    "predict_demo",
    "load_dataset", "get_dataset_stats",
    "save_audio", "audio_duration", "top_k_predictions",
]
