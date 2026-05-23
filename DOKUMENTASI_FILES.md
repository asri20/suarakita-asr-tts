# 📚 Dokumentasi Lengkap File Proyek SuaraKita ASR-TTS

**Tanggal:** May 23, 2026  
**Status:** Analisis Lengkap

---

## 📋 Daftar Isi
1. [File-File Terpakai](#file-file-terpakai)
2. [File-File Tidak Terpakai](#file-file-tidak-terpakai)
3. [Struktur Modul](#struktur-modul)
4. [Dependency Graph](#dependency-graph)

---

## ✅ FILE-FILE TERPAKAI

### 1. 🎯 `app.py` — Aplikasi Utama Streamlit

**Lokasi:** `/app.py`  
**Status:** ✅ DIGUNAKAN & BERFUNGSI BAIK  
**Tipe:** Entry point aplikasi web

#### Fungsi & Kelas:
```python
render_prediction(audio_bytes, model_ready) → None
```
- Menampilkan hasil prediksi ASR di UI
- Menampilkan waveform, MFCC, dan confidence chart

#### Fitur Utama:
- **Navigasi Sidebar** dengan 4 halaman (Beranda, ASR, TTS, Tentang)
- **Custom CSS** dengan dark theme dan gradient design
- **Integrasi ASR Module** untuk real-time speech recognition
- **Integrasi TTS Module** untuk text-to-speech generation
- **Responsive UI** dengan st.columns dan st.expander

#### Dependencies Impor:
```python
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from asr import (LABELS, SAMPLE_RATE, preprocess_bytes, preprocess_audio, 
                 load_audio_from_bytes, extract_mfcc, plot_mfcc, 
                 plot_confidence, predict_from_bytes, predict_demo, 
                 is_model_available)
from tts import (generate_speech_bytes, list_voices, list_speeds, 
                 list_volumes, get_voice_id, get_speed_value, get_volume_value)
```

---

### 2. 📦 `asr/__init__.py` — Inisialisasi Package ASR

**Lokasi:** `/asr/__init__.py`  
**Status:** ✅ DIGUNAKAN  
**Tipe:** Package initializer

#### Fungsi Utama:
- **Central import point** untuk semua ASR functions
- Mengexport public API dari 4 submodule (preprocess, feature_extraction, predict, utils)
- Memungkinkan `from asr import ...` pattern

#### Public API Yang Diexport:
```python
# Constants
LABELS, SAMPLE_RATE, N_MFCC, MAX_LEN, DURATION

# Audio Loading & Processing
load_audio, load_audio_from_bytes, normalize_audio, trim_silence, 
pad_or_truncate, preprocess_audio, preprocess_file, preprocess_bytes

# Feature Extraction
extract_mfcc, extract_mfcc_from_file, extract_mfcc_from_bytes, 
plot_mfcc, plot_confidence

# Model & Prediction
load_model, is_model_available, predict_from_audio, predict_from_bytes, 
predict_from_file, predict_demo, create_demo_model

# Utilities & Dataset
load_dataset, get_dataset_stats, save_audio, audio_duration, 
top_k_predictions, model_summary_text, get_label_index, get_label_from_index
```

---

### 3. 🔊 `asr/preprocess.py` — Preprocessing Audio

**Lokasi:** `/asr/preprocess.py`  
**Status:** ✅ DIGUNAKAN & CORE FUNCTIONALITY  
**Tipe:** Audio processing module

#### Konstanta Global:
```python
SAMPLE_RATE = 16000          # Hz, sampling rate standard
DURATION = 2.0               # detik, target durasi audio
N_MFCC = 13                  # Jumlah MFCC coefficients
MAX_LEN = 32                 # Jumlah frames
LABELS = [
    "ambil", "berhenti", "cepat", "kanan", "kiri",
    "lambat", "lepas", "maju", "mulai", "mundur"
]  # 10 robot control commands dalam Bahasa Indonesia
```

#### Fungsi-Fungsi Utama:

| Fungsi | Input | Output | Kegunaan |
|--------|-------|--------|----------|
| `load_audio(file_path, sr)` | str, int | np.ndarray | Load file audio, resample ke sample rate tertentu |
| `load_audio_from_bytes(audio_bytes, sr)` | bytes, int | np.ndarray | Load audio dari bytes (file upload), resample |
| `normalize_audio(audio)` | np.ndarray | np.ndarray | Normalisasi amplitude ke range [-1, 1] |
| `trim_silence(audio, top_db)` | np.ndarray, int | np.ndarray | Hapus silence dari awal dan akhir audio |
| `pad_or_truncate(audio, sr, duration)` | np.ndarray, int, float | np.ndarray | Pad dengan zeros atau truncate audio ke durasi fixed (2 detik) |
| `preprocess_audio(audio, sr)` | np.ndarray, int | np.ndarray | Full pipeline: normalize → trim silence → pad_or_truncate |
| `preprocess_file(file_path)` | str | np.ndarray | Load + preprocess file audio |
| `preprocess_bytes(audio_bytes)` | bytes | np.ndarray | Load + preprocess audio bytes |
| `get_label_index(label)` | str | int | Convert label string → index (0-9) |
| `get_label_from_index(index)` | int | str | Convert index (0-9) → label string |

#### Pipeline Preprocessing:
```
Raw Audio → Normalize → Trim Silence → Pad/Truncate (2s) → Ready for MFCC
```

#### Digunakan Oleh:
- `app.py` — preprocessing input user
- `asr/feature_extraction.py` — menggunakan constants dan fungsi
- `asr/predict.py` — preprocessing sebelum inferensi
- `asr/utils.py` — dataset loading

---

### 4. 🎵 `asr/feature_extraction.py` — Ekstraksi Fitur MFCC

**Lokasi:** `/asr/feature_extraction.py`  
**Status:** ✅ DIGUNAKAN & CORE FUNCTIONALITY  
**Tipe:** Feature extraction module

#### Fungsi-Fungsi Utama:

| Fungsi | Input | Output | Kegunaan |
|--------|-------|--------|----------|
| `extract_mfcc(audio, sr, n_mfcc, max_len)` | np.ndarray, int, int, int | np.ndarray (32, 13) | Ekstrak MFCC features menggunakan librosa |
| `extract_mfcc_from_file(file_path)` | str | np.ndarray (32, 13) | Load file + extract MFCC |
| `extract_mfcc_from_bytes(audio_bytes)` | bytes | np.ndarray (32, 13) | Load bytes + extract MFCC |
| `plot_mfcc(audio, sr, n_mfcc, title)` | np.ndarray, int, int, str | plt.Figure | Visualisasi waveform + MFCC heatmap |
| `plot_confidence(labels, probs)` | list, np.ndarray | plt.Figure | Bar chart confidence score untuk setiap label |

#### Output Shape:
```python
# MFCC output shape: (MAX_LEN, N_MFCC) = (32, 13)
# 32 frames × 13 MFCC coefficients
```

#### Kegunaan MFCC:
- **MFCC (Mel-Frequency Cepstral Coefficients)** adalah feature representation audio
- Meniru cara manusia mendengar (mel-scale frequency)
- Dimensionalitas lebih kecil dari raw audio, lebih cocok untuk ML
- 32 frames × 13 coef = input dimensi untuk CNN 1D model

#### Digunakan Oleh:
- `app.py` — visualisasi MFCC di UI
- `asr/predict.py` — extract MFCC sebelum prediction
- `asr/utils.py` — extract MFCC saat loading dataset

---

### 5. 🧠 `asr/predict.py` — Model Inference

**Lokasi:** `/asr/predict.py`  
**Status:** ✅ DIGUNAKAN & CORE FUNCTIONALITY  
**Tipe:** Inference module dengan singleton pattern

#### Global State:
```python
_model = None  # Singleton cache untuk model
_model_path = Path(__file__).parent / "model" / "model_asr.h5"
```

#### Fungsi-Fungsi Utama:

| Fungsi | Input | Output | Kegunaan |
|--------|-------|--------|----------|
| `load_model(model_path)` | str/Path/None | tf.keras.Model | Load model CNN 1D dari file .h5, cache di memory |
| `is_model_available(model_path)` | str/Path/None | bool | Check file .h5 exists |
| `predict_from_audio(audio, model)` | np.ndarray, Model | dict | Predict dari audio array |
| `predict_from_bytes(audio_bytes, model)` | bytes, Model | dict | Predict dari audio bytes (user upload) |
| `predict_from_file(file_path, model)` | str/Path, Model | dict | Predict dari file path |
| `create_demo_model()` | - | tf.keras.Model | Buat model demo dengan weights random |
| `predict_demo(audio)` | np.ndarray | dict | Predict tanpa training (demo mode) |

#### Return Value Structure:
```python
{
    "label": str,                    # e.g., "maju"
    "label_capitalized": str,        # e.g., "Maju"
    "confidence": float,             # 0.0 - 1.0
    "confidence_pct": float,         # 0.0 - 100.0
    "probabilities": np.ndarray,     # Shape (10,), softmax output
    "top_k": list,                   # [(label, prob), ...] top 5
    "mfcc": np.ndarray,              # Shape (32, 13)
    "audio": np.ndarray,             # Preprocessed audio
}
```

#### Model Architecture:
```
Input (32, 13, 1) → Conv1D → MaxPool → Conv1D → Flatten → Dense → Softmax
Output: 10 classes (LABELS)
```

#### Digunakan Oleh:
- `app.py` — `predict_from_bytes()`, `predict_demo()`, `is_model_available()`

---

### 6. 🛠️ `asr/utils.py` — Utility Functions

**Lokasi:** `/asr/utils.py`  
**Status:** ✅ DIGUNAKAN  
**Tipe:** Utility module

#### Fungsi-Fungsi Utama:

| Fungsi | Input | Output | Kegunaan |
|--------|-------|--------|----------|
| `load_dataset(dataset_dir)` | str/Path | (X, y) | Load seluruh dataset dari folder struktur |
| `get_dataset_stats(dataset_dir)` | str/Path | dict | Hitung jumlah file per class |
| `save_audio(audio, file_path, sr)` | np.ndarray, str, int | None | Simpan audio array → WAV file |
| `audio_duration(audio, sr)` | np.ndarray, int | float | Hitung durasi audio dalam detik |
| `top_k_predictions(probs, k)` | np.ndarray, int | list | Get top-k index dengan confidence |
| `model_summary_text(model)` | tf.keras.Model | str | Dapatkan model summary sebagai string |

#### Kegunaan:
- Support untuk training scripts dan data exploration
- Dataset loading untuk model training
- Statistical analysis untuk dataset quality

#### Digunakan Oleh:
- Training notebooks (potentially)
- `asr/predict.py` — `top_k_predictions()`
- `asr/__init__.py` — re-export

---

### 7. 📦 `tts/__init__.py` — Inisialisasi Package TTS

**Lokasi:** `/tts/__init__.py`  
**Status:** ✅ DIGUNAKAN  
**Tipe:** Package initializer

#### Public API Yang Diexport:
```python
# Core Functions
generate_speech, generate_speech_bytes, list_available_voices, clean_old_audio

# Voice Configuration
VOICES, SPEED_OPTIONS, VOLUME_OPTIONS, get_voice_id, get_speed_value, 
get_volume_value, list_voices, list_speeds, list_volumes, 
DEFAULT_VOICE, DEFAULT_SPEED
```

#### Memungkinkan:
```python
from tts import generate_speech_bytes, list_voices, get_voice_id
```

---

### 8. 🔊 `tts/generate.py` — TTS Generation

**Lokasi:** `/tts/generate.py`  
**Status:** ✅ DIGUNAKAN & CORE FUNCTIONALITY  
**Tipe:** TTS synthesis module

#### Konstanta:
```python
OUTPUT_DIR = Path(__file__).parent / "audio_output"  # Folder output MP3
```

#### Fungsi-Fungsi Utama:

| Fungsi | Input | Output | Kegunaan |
|--------|-------|--------|----------|
| `_generate_speech_async(text, voice, rate, volume, output_path)` | str, str, str, str, Path | str | [Internal] Async edge-tts synthesis |
| `generate_speech(text, voice, rate, volume, output_path)` | str, str, str, str, Path | str | Generate speech → MP3 file |
| `generate_speech_bytes(text, voice, rate, volume)` | str, str, str, str | bytes | Generate speech → MP3 bytes (no file) |
| `_list_voices_async()` | - | list | [Internal] Async fetch voices dari edge-tts |
| `list_available_voices()` | - | list | List voice Indonesia (wrapper sync) |
| `clean_old_audio(max_files)` | int | None | Hapus file audio lama, keep max N files |

#### Engine:
- **Microsoft Edge TTS** (`edge-tts` library)
- Gratis, high-quality neural voices
- Support Bahasa Indonesia dengan 2 voices (Gadis, Ardi)

#### Digunakan Oleh:
- `app.py` — `generate_speech_bytes()` untuk TTS page
- `tts/__init__.py` — re-export

---

### 9. 🎤 `tts/voices.py` — Konfigurasi Voice

**Lokasi:** `/tts/voices.py`  
**Status:** ✅ DIGUNAKAN  
**Tipe:** Configuration module

#### Konstanta Global:

```python
VOICES = {
    "Indonesia — Perempuan (Gadis)": "id-ID-GadisNeural",
    "Indonesia — Laki-laki (Ardi)": "id-ID-ArdiNeural",
    "English — Female (Jenny)": "en-US-JennyNeural",
    "English — Male (Ryan)": "en-US-RyanMultilingualNeural",
    "Jepang — Perempuan (Nanami)": "ja-JP-NanamiNeural",
    "Korea — Perempuan (SunHi)": "ko-KR-SunHiNeural",
}

SPEED_OPTIONS = {
    "Lambat": "-20%",
    "Normal": "+0%",
    "Cepat": "+25%",
    "Sangat Cepat": "+50%",
}

VOLUME_OPTIONS = {
    "Pelan": "-20%",
    "Normal": "+0%",
    "Keras": "+20%",
}

DEFAULT_VOICE = "id-ID-GadisNeural"
DEFAULT_SPEED = "+0%"
DEFAULT_VOLUME = "+0%"
```

#### Fungsi-Fungsi Utama:

| Fungsi | Input | Output | Kegunaan |
|--------|-------|--------|----------|
| `get_voice_id(display_name)` | str | str | Map display name → voice ID |
| `get_speed_value(display_name)` | str | str | Map display name → speed value |
| `get_volume_value(display_name)` | str | str | Map display name → volume value |
| `list_voices()` | - | list | Get semua voice display names |
| `list_speeds()` | - | list | Get semua speed display names |
| `list_volumes()` | - | list | Get semua volume display names |

#### Digunakan Oleh:
- `app.py` — dropdown selection & voice configuration
- `tts/generate.py` — menggunakan DEFAULT constants
- `tts/__init__.py` — re-export

---

### 10. 🔧 `assets/convert_dataset.py` — Dataset Conversion

**Lokasi:** `/assets/convert_dataset.py`  
**Status:** ✅ SCRIPT STANDALONE  
**Tipe:** Setup/utility script

#### Fungsi:
- Convert format audio dari M4A/MP3 → WAV
- Normalize ke mono, 16kHz sample rate
- Sesuai dengan requirement ASR model

#### Penggunaan:
```bash
# Jalankan satu kali saat setup data awal
python assets/convert_dataset.py
```

#### Kode Sederhana:
```python
from pydub import AudioSegment
from pathlib import Path

DATASET_DIR = Path(r"E:\S1Informatika\PTU\suarakita-asr-tts\asr\dataset")

for audio_path in DATASET_DIR.rglob("*.m4a") + DATASET_DIR.rglob("*.mp3"):
    # Convert ke WAV (mono, 16kHz)
    audio = AudioSegment.from_file(audio_path, format=ext)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(audio_path.with_suffix(".wav"), format="wav")
    audio_path.unlink()  # Hapus file original
```

#### Digunakan Oleh:
- Manual execution saat setup proyek awal

---

## ❌ FILE-FILE TIDAK TERPAKAI

### 1. ⚠️ `tts/google_tts.py` — UNUSED & DAPAT DIHAPUS

**Lokasi:** `/tts/google_tts.py`  
**Status:** ❌ **NOT USED - DAPAT DIHAPUS**  
**Tipe:** Alternative TTS implementation

#### Masalah:
- ❌ **Tidak di-import** di `tts/__init__.py`
- ❌ **Tidak digunakan** di `app.py` atau file manapun
- ⚠️ Proyek menggunakan Microsoft `edge-tts`, bukan Google TTS
- ⚠️ Dependency `google-cloud-texttospeech` tercantum di requirements.txt tapi tidak digunakan

#### Rekomendasi Aksi:
```bash
# 1. Hapus file
rm tts/google_tts.py

# 2. Update requirements.txt - hapus baris:
# google-cloud-texttospeech
```

---

### 2. ❌ `asr/export_mfcc.py` — ERROR & BROKEN

**Lokasi:** `/asr/export_mfcc.py`  
**Status:** ❌ **BROKEN IMPORT - TIDAK BERFUNGSI**  
**Tipe:** Utility script (dimaksudkan sebagai standalone)

#### Masalah Kritis:
```python
from asr.feature_extraction import export_mfcc_to_csv  # ← ERROR!
# Function export_mfcc_to_csv() TIDAK ADA di feature_extraction.py
```

- ❌ **ImportError** jika dijalankan
- ❌ **Tidak digunakan** dimana pun dalam proyek
- ❌ Function `export_mfcc_to_csv()` tidak pernah diimplementasikan

#### Rekomendasi Aksi:

**Opsi A — Implement (jika ingin feature):**
```python
# Tambahkan ke asr/feature_extraction.py
def export_mfcc_to_csv(audio_bytes, output_path):
    """
    Extract MFCC dari audio bytes dan simpan ke CSV file
    """
    mfcc = extract_mfcc_from_bytes(audio_bytes)
    np.savetxt(output_path, mfcc, delimiter=',')
```

**Opsi B — Hapus (jika tidak diperlukan):**
```bash
rm asr/export_mfcc.py
```

---

## 📊 STRUKTUR MODUL

### ASR Module (`asr/`)
```
asr/
├── __init__.py              ← Central API export
├── preprocess.py            ← Audio loading & preprocessing
├── feature_extraction.py     ← MFCC extraction & visualization
├── predict.py               ← Model inference
├── utils.py                 ← Dataset utilities
├── export_mfcc.py           ❌ BROKEN - Not used
└── model/
    ├── model_asr.h5         ← Trained CNN 1D model
    ├── labels.json          ← Label mapping
    └── mfcc_features/       ← Cached MFCC CSV files
        ├── ambil/           ← MFCC features untuk class "ambil"
        ├── berhenti/        ← MFCC features untuk class "berhenti"
        └── ... (8 classes lagi)
```

#### ASR Processing Pipeline:
```
Audio Input (WAV/MP3/bytes)
    ↓
preprocess.py: Load → Normalize → Trim Silence → Pad/Truncate
    ↓
feature_extraction.py: Extract MFCC (32, 13)
    ↓
predict.py: CNN 1D Inference
    ↓
Output: {label, confidence, probabilities, top_k}
```

---

### TTS Module (`tts/`)
```
tts/
├── __init__.py              ← Central API export
├── generate.py              ← Speech synthesis (edge-tts)
├── voices.py                ← Voice configuration & mapping
├── google_tts.py            ❌ UNUSED - Can be deleted
└── audio_output/            ← Generated MP3 files cache
    └── *.mp3
```

#### TTS Processing Pipeline:
```
Text Input (Bahasa Indonesia)
    ↓
generate.py: Use Microsoft edge-tts
    ↓
voices.py: Select voice, speed, volume
    ↓
Output: MP3 bytes (or file)
```

---

## 🔗 DEPENDENCY GRAPH

```
📱 app.py (ENTRY POINT)
│
├────→ asr/__init__.py (Central ASR API)
│       ├────→ asr/preprocess.py
│       │       └─ load_audio, load_audio_from_bytes, normalize_audio,
│       │          trim_silence, pad_or_truncate, preprocess_audio,
│       │          preprocess_bytes, LABELS, SAMPLE_RATE, N_MFCC, MAX_LEN
│       │
│       ├────→ asr/feature_extraction.py
│       │       └─ extract_mfcc, extract_mfcc_from_bytes, plot_mfcc,
│       │          plot_confidence
│       │       (depends on: preprocess.py constants)
│       │
│       ├────→ asr/predict.py
│       │       └─ load_model, is_model_available, predict_from_bytes,
│       │          predict_demo, create_demo_model
│       │       (depends on: preprocess.py, feature_extraction.py, utils.py)
│       │
│       └────→ asr/utils.py
│               └─ load_dataset, get_dataset_stats, save_audio,
│                  audio_duration, top_k_predictions, model_summary_text
│               (depends on: preprocess.py, feature_extraction.py)
│
└────→ tts/__init__.py (Central TTS API)
        ├────→ tts/generate.py
        │       └─ generate_speech, generate_speech_bytes,
        │          list_available_voices, clean_old_audio
        │       (depends on: voices.py)
        │
        └────→ tts/voices.py
                └─ VOICES, SPEED_OPTIONS, VOLUME_OPTIONS,
                   get_voice_id, get_speed_value, get_volume_value,
                   list_voices, list_speeds, list_volumes
```

---

## 📈 Summary Table

| File | Lokasi | Status | Digunakan | Fungsi Utama |
|------|--------|--------|-----------|--------------|
| **app.py** | `/` | ✅ | Ya | Main Streamlit web app |
| **asr/__init__.py** | `/asr/` | ✅ | Ya | Central ASR API |
| **preprocess.py** | `/asr/` | ✅ | Ya | Audio preprocessing |
| **feature_extraction.py** | `/asr/` | ✅ | Ya | MFCC extraction |
| **predict.py** | `/asr/` | ✅ | Ya | Model inference |
| **utils.py** | `/asr/` | ✅ | Ya | Dataset utilities |
| **export_mfcc.py** | `/asr/` | ❌ | Tidak | ⚠️ ERROR: broken import |
| **tts/__init__.py** | `/tts/` | ✅ | Ya | Central TTS API |
| **generate.py** | `/tts/` | ✅ | Ya | TTS synthesis |
| **voices.py** | `/tts/` | ✅ | Ya | Voice configuration |
| **google_tts.py** | `/tts/` | ❌ | Tidak | ⚠️ UNUSED: can delete |
| **convert_dataset.py** | `/assets/` | ✅ | Standalone | Dataset conversion |

---

## 🎯 ACTION ITEMS

### Priority 1 (HIGH)
- [ ] **Hapus** `tts/google_tts.py` — tidak digunakan
- [ ] **Update** `requirements.txt` — hapus `google-cloud-texttospeech`
- [ ] **Fix atau Hapus** `asr/export_mfcc.py` — broken import

### Priority 2 (MEDIUM)
- [ ] Verifikasi metadata — app menampilkan 12 kelas tapi LABELS hanya 10
- [ ] Add docstrings untuk semua public functions
- [ ] Add type hints untuk parameter functions

### Priority 3 (LOW)
- [ ] Optimize MFCC caching di `model/mfcc_features/`
- [ ] Add logging untuk troubleshooting
- [ ] Add unit tests untuk ASR module

---

**Generated:** May 23, 2026  
**Proyek Status:** ✅ Mostly Production-Ready (dengan 2 issues minor)
