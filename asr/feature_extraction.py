"""
feature_extraction.py - Ekstraksi fitur MFCC untuk ASR
Menggunakan librosa untuk komputasi MFCC
"""

import numpy as np
import librosa
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import os
from pathlib import Path
from .preprocess import SAMPLE_RATE, N_MFCC, MAX_LEN


def extract_mfcc(audio: np.ndarray, sr: int = SAMPLE_RATE,
                 n_mfcc: int = N_MFCC, max_len: int = MAX_LEN) -> np.ndarray:
    """
    Ekstrak fitur MFCC dari sinyal audio.
    
    Returns:
        mfcc_padded: array shape (max_len, n_mfcc)
    """
    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=n_mfcc,
        n_fft=512,
        hop_length=512,
        n_mels=40
    )
    # Transpose: (n_mfcc, T) → (T, n_mfcc)
    mfcc = mfcc.T

    # Padding atau truncating agar shape konsisten
    if mfcc.shape[0] < max_len:
        pad_width = max_len - mfcc.shape[0]
        mfcc = np.pad(mfcc, ((0, pad_width), (0, 0)), mode='constant')
    else:
        mfcc = mfcc[:max_len, :]

    return mfcc  # shape: (max_len, n_mfcc)


def extract_mfcc_from_file(file_path: str) -> np.ndarray:
    """Ekstrak MFCC langsung dari file audio."""
    from .preprocess import preprocess_file
    audio = preprocess_file(file_path)
    return extract_mfcc(audio)


def extract_mfcc_from_bytes(audio_bytes: bytes) -> np.ndarray:
    """Ekstrak MFCC dari audio bytes."""
    from .preprocess import preprocess_bytes
    audio = preprocess_bytes(audio_bytes)
    return extract_mfcc(audio)


def plot_mfcc(audio: np.ndarray, sr: int = SAMPLE_RATE,
              n_mfcc: int = N_MFCC, title: str = "MFCC Feature Map") -> plt.Figure:
    """
    Buat visualisasi MFCC yang modern dan menarik.
    
    Returns:
        matplotlib Figure object
    """
    mfcc_raw = librosa.feature.mfcc(
        y=audio, sr=sr, n_mfcc=n_mfcc,
        n_fft=512, hop_length=512, n_mels=40
    )

    fig, axes = plt.subplots(2, 1, figsize=(10, 6),
                             facecolor='#0D1117')
    fig.subplots_adjust(hspace=0.4)

    # ── Plot 1: Waveform ──────────────────────────────────
    ax1 = axes[0]
    ax1.set_facecolor('#161B22')
    times = np.linspace(0, len(audio) / sr, len(audio))
    ax1.plot(times, audio, color='#58A6FF', linewidth=0.8, alpha=0.9)
    ax1.fill_between(times, audio, alpha=0.15, color='#58A6FF')
    ax1.set_title('Sinyal Audio (Waveform)', color='#E6EDF3',
                  fontsize=11, fontweight='bold', pad=8)
    ax1.set_xlabel('Waktu (detik)', color='#8B949E', fontsize=9)
    ax1.set_ylabel('Amplitudo', color='#8B949E', fontsize=9)
    ax1.tick_params(colors='#8B949E', labelsize=8)
    for spine in ax1.spines.values():
        spine.set_edgecolor('#30363D')
    ax1.grid(True, color='#21262D', linewidth=0.5, alpha=0.7)

    # ── Plot 2: MFCC Heatmap ─────────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor('#161B22')
    img = librosa.display.specshow(
        mfcc_raw,
        x_axis='time',
        sr=sr,
        hop_length=512,
        ax=ax2,
        cmap='magma'
    )
    fig.colorbar(img, ax=ax2, format='%+2.0f',
                 label='Nilai MFCC').ax.yaxis.label.set_color('#8B949E')
    ax2.set_title('MFCC Coefficients (13 features)', color='#E6EDF3',
                  fontsize=11, fontweight='bold', pad=8)
    ax2.set_xlabel('Waktu (detik)', color='#8B949E', fontsize=9)
    ax2.set_ylabel('Koefisien MFCC', color='#8B949E', fontsize=9)
    ax2.tick_params(colors='#8B949E', labelsize=8)
    for spine in ax2.spines.values():
        spine.set_edgecolor('#30363D')

    fig.suptitle(title, color='#F0F6FC', fontsize=13,
                 fontweight='bold', y=1.01)
    return fig


def plot_confidence(labels: list, probs: np.ndarray) -> plt.Figure:
    """
    Visualisasi confidence score sebagai bar chart horizontal.
    """
    sorted_idx = np.argsort(probs)[::-1][:6]  # Top 6
    top_labels = [labels[i].capitalize() for i in sorted_idx]
    top_probs = probs[sorted_idx] * 100

    fig, ax = plt.subplots(figsize=(8, 4), facecolor='#0D1117')
    ax.set_facecolor('#161B22')

    colors = ['#3FB950' if i == 0 else '#58A6FF' for i in range(len(top_labels))]
    bars = ax.barh(top_labels[::-1], top_probs[::-1],
                   color=colors[::-1], height=0.6,
                   edgecolor='none')

    for bar, prob in zip(bars, top_probs[::-1]):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f'{prob:.1f}%', va='center', ha='left',
                color='#E6EDF3', fontsize=10, fontweight='bold')

    ax.set_xlim(0, 115)
    ax.set_xlabel('Confidence (%)', color='#8B949E', fontsize=9)
    ax.set_title('Top Prediksi — Confidence Score', color='#E6EDF3',
                 fontsize=11, fontweight='bold', pad=10)
    ax.tick_params(colors='#8B949E', labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363D')
    ax.grid(True, axis='x', color='#21262D', linewidth=0.5, alpha=0.7)

    fig.tight_layout()
    return fig


def export_mfcc_to_csv(output_dir: str = None, base_dataset_dir: str = None) -> None:
    """
    Export semua MFCC features dari dataset ke CSV format.
    
    Args:
        output_dir: Direktori output untuk CSV files (default: asr/model/mfcc_features/)
        base_dataset_dir: Direktori dataset (default: asr/dataset/)
    
    Example:
        from asr.feature_extraction import export_mfcc_to_csv
        export_mfcc_to_csv()
    """
    # Set default paths
    if output_dir is None:
        output_dir = Path(__file__).parent / "model" / "mfcc_features"
    else:
        output_dir = Path(output_dir)
    
    if base_dataset_dir is None:
        base_dataset_dir = Path(__file__).parent / "dataset"
    else:
        base_dataset_dir = Path(base_dataset_dir)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not base_dataset_dir.exists():
        raise ValueError(f"Dataset directory tidak ditemukan: {base_dataset_dir}")
    
    print(f"[MFCC Export] Memproses dataset dari: {base_dataset_dir}")
    print(f"[MFCC Export] Output akan disimpan di: {output_dir}")
    print("-" * 70)
    
    total_files = 0
    total_classes = 0
    
    # Iterasi semua class folders
    class_folders = sorted([f for f in base_dataset_dir.iterdir() if f.is_dir()])
    
    if not class_folders:
        raise ValueError(f"Tidak ada folder class di: {base_dataset_dir}")
    
    for class_folder in class_folders:
        class_name = class_folder.name
        class_output_dir = output_dir / class_name
        class_output_dir.mkdir(parents=True, exist_ok=True)
        
        wav_files = sorted(class_folder.glob("*.wav"))
        total_classes += 1
        
        print(f"\n📁 Class: '{class_name}' ({len(wav_files)} files)")
        
        for idx, wav_file in enumerate(wav_files, 1):
            try:
                # Extract MFCC
                mfcc = extract_mfcc_from_file(str(wav_file))
                
                # Convert to DataFrame
                # mfcc shape: (MAX_LEN, N_MFCC) = (32, 13)
                column_names = [f'mfcc_{i}' for i in range(mfcc.shape[1])]
                df = pd.DataFrame(mfcc, columns=column_names)
                
                # Add metadata columns
                df.insert(0, 'frame_id', range(len(df)))
                df.insert(1, 'class', class_name)
                df.insert(2, 'file', wav_file.stem)
                
                # Save to CSV
                csv_filename = f"{wav_file.stem}_mfcc.csv"
                csv_path = class_output_dir / csv_filename
                df.to_csv(csv_path, index=False)
                
                total_files += 1
                
                if idx % 5 == 0 or idx == len(wav_files):
                    print(f"  ✓ Processed {idx}/{len(wav_files)}: {wav_file.name}")
                    
            except Exception as e:
                print(f"  ✗ Error processing {wav_file.name}: {e}")
    
    print("-" * 70)
    print(f"\n✅ Export selesai!")
    print(f"   Total classes: {total_classes}")
    print(f"   Total files: {total_files}")
    print(f"   Output directory: {output_dir}")
    print(f"\n📊 Struktur CSV:")
    print(f"   - frame_id: ID frame (0-31)")
    print(f"   - class: Nama class")
    print(f"   - file: Nama file audio")
    print(f"   - mfcc_0 sampai mfcc_12: 13 MFCC coefficients")
