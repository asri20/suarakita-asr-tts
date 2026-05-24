# 🎙️ SuaraKita — ASR & TTS Bahasa Indonesia

Aplikasi web berbasis **Streamlit** yang menggabungkan **Automatic Speech Recognition (ASR)** dan **Text-to-Speech (TTS)** untuk Bahasa Indonesia. Dirancang untuk **robot control commands** dengan real-time speech recognition dan natural neural voice synthesis.

## 🎯 Use Case
Aplikasi ini menggunakan teknologi **deep learning** untuk:
- 🤖 **Mengenali perintah suara Bahasa Indonesia** untuk kontrol robot (ambil, maju, mundur, dll)
- 🔊 **Mengubah teks menjadi suara natural** dengan pilihan berbagai voice
- 📊 **Visualisasi real-time** untuk MFCC features dan confidence scores

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🎤 **ASR (Speech Recognition)** | Prediksi 10 robot commands dari audio menggunakan CNN 1D + MFCC features |
| 🔊 **TTS (Text-to-Speech)** | Konversi teks Bahasa Indonesia ke suara natural menggunakan Microsoft edge-tts |
| 📊 **Visualisasi MFCC** | Waveform dan MFCC spectrogram dalam real-time |
| 📈 **Confidence Score** | Bar chart showing confidence untuk setiap label |
| 🎙️ **Recording Input** | Microphone recording langsung dari browser |
| 📁 **File Upload** | Support upload file audio (WAV, MP3, M4A) |
| 🎵 **Audio Download** | Download hasil TTS sebagai file MP3 |
| 🎨 **Dark Theme UI** | Modern responsive design dengan Streamlit |

---

## 🏗️ Struktur Proyek

```
suarakita-asr-tts/
│
├── app.py                      # 🎯 Aplikasi utama Streamlit
├── requirements.txt            # Python dependencies
├── README.md                   # Dokumentasi utama
│
├── 📚 DOKUMENTASI_FILES.md     # Dokumentasi lengkap setiap file (NEW!)
│
├── asr/                        # 📦 ASR Module (Speech Recognition)
│   ├── __init__.py             # Package initializer
│   ├── preprocess.py           # Audio loading, normalize, trim, pad
│   ├── feature_extraction.py   # MFCC extraction & visualization
│   ├── predict.py              # CNN 1D model inference
│   ├── utils.py                # Dataset loading & utilities
│   ├── export_mfcc.py          # ⚠️ DEPRECATED (broken imports)
│   │
│   ├── dataset/                # 📁 Dataset storage (10 robot commands)
│   │   ├── ambil/              # Grab
│   │   ├── berhenti/           # Stop
│   │   ├── cepat/              # Fast
│   │   ├── kanan/              # Right
│   │   ├── kiri/               # Left
│   │   ├── lambat/             # Slow
│   │   ├── lepas/              # Release
│   │   ├── maju/               # Forward
│   │   ├── mulai/              # Start
│   │   └── mundur/             # Backward
│   │
│   ├── model/
│   │   ├── model_asr.h5        # 🧠 Trained CNN 1D model
│   │   ├── labels.json         # Label mapping (10 classes)
│   │   └── mfcc_features/      # Pre-extracted MFCC cache
│   │
│   └── training/
│       ├── asr_training.ipynb  # 📓 Training notebook
│       └── train_asr_cnn.py    # Training script
│
├── tts/                        # 📦 TTS Module (Text-to-Speech)
│   ├── __init__.py             # Package initializer
│   ├── generate.py             # Speech synthesis (edge-tts)
│   ├── voices.py               # Voice & speed configuration
│   └── audio_output/           # Generated MP3 cache
│
├── audio/                      # 🎵 Temporary recording files
├── assets/                     # 🛠️ Utility scripts
│   └── convert_dataset.py      # Dataset conversion (M4A/MP3 → WAV)
│
└── .env.example                # Environment variables (optional)
```

---

## 🎯 Dataset & Labels

**Saat ini proyek menggunakan 10 robot control commands:**

| # | Command | Indonesian |
|---|---------|------------|
| 1 | `ambil` | Ambil |
| 2 | `berhenti` | Berhenti |
| 3 | `cepat` | Cepat |
| 4 | `kanan` | Kanan |
| 5 | `kiri` | Kiri |
| 6 | `lambat` | Lambat |
| 7 | `lepas` | Lepas |
| 8 | `maju` | Maju |
| 9 | `mulai` | Mulai |
| 10 | `mundur` | Mundur |

**Format Audio Dataset:**
- 📁 Setiap folder berisi 35-50 file audio `.wav`
- 🎵 Format: WAV, 16kHz, mono, durasi 1-2 detik
- 📊 Total: ~350-500 audio files untuk training/validation

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/[username]/suarakita-asr-tts.git
cd suarakita-asr-tts
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
streamlit run app.py
```

Aplikasi akan buka di `http://localhost:8501`

### 4. Training Model (Optional)
Jika ingin retrain model dengan dataset baru:
```bash
# Buka training notebook
jupyter notebook asr/training/asr_training.ipynb

# Atau jalankan script
python asr/training/train_asr_cnn.py
```

---

## 📖 Documentation

**File dokumentasi lengkap tersedia:**

- 📄 **[DOKUMENTASI_FILES.md](DOKUMENTASI_FILES.md)** - Detail lengkap setiap file dan fungsi

---

## 🧠 ASR: CNN 1D Model Architecture

**Input**: MFCC features dengan shape (batch_size, 32, 13)
- 32: Time frames dari audio 2-detik @ 16kHz
- 13: MFCC coefficients

**Architecture**:
```
Input (32, 13, 1)
  ↓
Conv1D(32 filters, kernel=3, padding='same')
  ↓ ReLU activation
  ↓
MaxPooling1D(pool_size=2)
  ↓ Dropout(0.3)
  ↓
Conv1D(64 filters, kernel=3, padding='same')
  ↓ ReLU activation
  ↓
GlobalAveragePooling1D()
  ↓ Dropout(0.3)
  ↓
Dense(128, ReLU)
  ↓ Dropout(0.2)
  ↓
Dense(10, softmax)  ← 10 output classes
```

**Performance**:
- Input shapes: (batch, 32, 13)
- Output: Softmax probabilities over 10 classes
- Training: ~50 epochs, validation split 0.2

---

## 🔊 TTS: Microsoft Edge-TTS Features

**Supported Voices** (Bahasa Indonesia):
- 👩 **Gadis Neural** - Female voice (natural & expressive)
- 👨 **Ardi Neural** - Male voice (natural & clear)

**Speed Options**:
- Lambat: -20%
- Normal: +0% (default)
- Cepat: +25%
- Sangat Cepat: +50%

**Volume Options**:
- Pelan: -20%
- Normal: +0% (default)
- Keras: +20%

**Technology**:
- Engine: Microsoft edge-tts (free, no API key required)
- Format: MP3 (high quality)
- Async processing: ✅ Non-blocking synthesis

---

## 📊 MFCC Feature Extraction

**What is MFCC?**
- Mel-Frequency Cepstral Coefficients
- Mimics human hearing response (mel-scale frequency)
- Extracted untuk setiap 50ms window dari audio

**Extraction Parameters**:
```python
SAMPLE_RATE = 16000 Hz      # Standard audio sampling
N_MFCC = 13                 # Number of coefficients
MAX_LEN = 32                # Number of time frames
DURATION = 2.0              # Target audio duration (seconds)
```

**Output Shape**: (32, 13)
- 32 frames × 13 MFCC coefficients = 416 features
- Input ke CNN 1D model untuk classification

---

## 💻 Requirements & Dependencies

**Python**: 3.8+

**Core Dependencies**:
- `streamlit >= 1.32.0` - Web framework
- `numpy >= 1.24.0` - Numerical computing
- `librosa >= 0.10.0` - Audio feature extraction (MFCC)
- `matplotlib >= 3.7.0` - Visualization

**ML Dependencies**:
- `tensorflow >= 2.10.0` - Deep learning (optional, commented in requirements)
- `keras` - Neural networks (included with TensorFlow)
- `scikit-learn >= 1.3.0` - ML utilities

**Audio Processing**:
- `sounddevice >= 0.4.6` - Audio device recording
- `soundfile >= 0.12.1` - Audio file I/O (WAV)
- `pydub >= 0.25.1` - Audio format conversion
- `edge-tts >= 6.1.9` - TTS synthesis

**UI & Utilities**:
- `streamlit-mic-recorder >= 0.0.4` - Microphone widget
- `plotly >= 5.15.0` - Interactive charts
- `pandas >= 2.0.0` - Data processing
- `python-dotenv` - Environment variables

**Install semua dependencies**:
```bash
pip install -r requirements.txt
```

---

## 🎮 Cara Menggunakan Aplikasi

### 🏠 Halaman Beranda
- Menampilkan hero section dengan fitur utama
- Statistik model dan dataset
- Informasi teknologi yang digunakan

### 🎤 Halaman Speech Recognition (ASR)

**3 cara input audio:**

1. **Microphone Recording** 📍
   - Klik tombol "Record from Microphone"
   - Berbicara dengan jelas (1-2 detik)
   - Sistem otomatis akan memproses

2. **File Upload** 📁
   - Upload file audio (WAV, MP3, M4A)
   - Format akan dikontrol otomatis
   - Durasi optimal: 1-2 detik

3. **Demo Mode** 🎯
   - Tes aplikasi tanpa model
   - Menggunakan demo predictions

**Output yang ditampilkan:**
- 🎵 Waveform visualization
- 📊 MFCC spectrogram (heatmap)
- ✅ Predicted label dengan confidence %
- 📈 Top-5 predictions dengan probabilities
- 📋 Full probability distribution

### 🔊 Halaman Text-to-Speech (TTS)

**Cara menggunakan:**

1. Input teks Bahasa Indonesia di text area
2. Pilih suara: Gadis (♀️) atau Ardi (♂️)
3. Pilih kecepatan: Lambat, Normal, Cepat, Sangat Cepat
4. Pilih volume: Pelan, Normal, Keras
5. Klik "Generate Suara"
6. Dengarkan preview MP3
7. Download MP3 (optional)

**Contoh teks:**
- "Ambil benda di depan sana"
- "Robot, maju ke depan"
- "Berhenti dan tunggu perintah"

### 📖 Halaman Tentang Proyek
- Informasi proyek dan tim developer
- Spesifikasi model dan dataset
- Links ke dokumentasi

---

## 🔌 API & Module Usage

### Menggunakan ASR Module

```python
from asr import (
    preprocess_bytes,
    extract_mfcc,
    predict_from_bytes,
    is_model_available
)

# Load audio dari bytes
audio_bytes = open('audio.wav', 'rb').read()

# Preprocess audio
audio = preprocess_bytes(audio_bytes)

# Extract MFCC features
mfcc = extract_mfcc(audio, sr=16000, n_mfcc=13, max_len=32)

# Predict
if is_model_available():
    result = predict_from_bytes(audio_bytes)
    print(f"Predicted: {result['label']} ({result['confidence_pct']:.1f}%)")
```

### Menggunakan TTS Module

```python
from tts import (
    generate_speech_bytes,
    list_voices,
    get_voice_id,
    get_speed_value,
    get_volume_value
)

# Generate speech bytes
text = "Halo dunia"
voice_id = get_voice_id("Indonesia — Perempuan (Gadis)")
speed = get_speed_value("Normal")
volume = get_volume_value("Normal")

mp3_bytes = generate_speech_bytes(
    text=text,
    voice=voice_id,
    rate=speed,
    volume=volume
)

# Save atau stream
with open('output.mp3', 'wb') as f:
    f.write(mp3_bytes)
```

---

## 📚 Module Documentation

Dokumentasi lengkap setiap module tersedia dalam file:
- **[DOKUMENTASI_FILES.md](DOKUMENTASI_FILES.md)** - Detail semua functions
- **[FUNGSI_REFERENCE.md](FUNGSI_REFERENCE.md)** - Quick reference

**Module Structure**:
```
asr/                    # Speech Recognition
├── preprocess.py      # Audio loading & preprocessing
├── feature_extraction # MFCC extraction & visualization
├── predict.py         # Model inference
└── utils.py           # Dataset utilities

tts/                    # Text-to-Speech
├── generate.py        # TTS synthesis
└── voices.py          # Voice configuration
```

---

## 🐛 Troubleshooting

### Model tidak loading
```
Error: Model file not found at asr/model/model_asr.h5
```
**Solution:**
- Pastikan file `model_asr.h5` ada di folder `asr/model/`
- Untuk demo, aplikasi bisa run tanpa model dengan "Demo Mode"

### Audio processing error
```
Error: Audio duration less than required
```
**Solution:**
- Durasi audio minimal: 1 detik
- Durasi optimal: 1-2 detik
- Format: WAV, 16kHz, mono

### TTS tidak berfungsi
```
Error: Cannot connect to edge-tts
```
**Solution:**
- Pastikan internet connection aktif
- Edge-tts memerlukan koneksi internet
- Coba gunakan VPN jika ada blocking

### Memory error saat loading dataset
```
MemoryError: Unable to allocate memory
```
**Solution:**
- Reduce dataset size untuk testing
- Gunakan batch processing untuk large datasets
- Pastikan RAM tersedia minimal 4GB

---

## 🔍 Known Issues & Limitations

### Metadata Mismatch ⚠️
- README lama menyebutkan 12 kelas (yesus, simon, dll)
- Model sekarang menggunakan 10 robot commands
- Status: Fixed in current version

### Unused Files ⚠️
- `tts/google_tts.py` - Not integrated, can be deleted
- `asr/export_mfcc.py` - Broken imports, needs fix
- Status: Documented di [ANALISIS_FILE_TIDAK_TERPAKAI.md](ANALISIS_FILE_TIDAK_TERPAKAI.md)

### Performance Notes
- First prediction might be slower (model loading)
- TTS synthesis depends on text length
- MFCC extraction takes ~100-200ms per audio

---

## 🛠️ Development & Contributing

### Setup Development Environment
```bash
# Clone repo
git clone https://github.com/[username]/suarakita-asr-tts.git
cd suarakita-asr-tts

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Install dev dependencies
pip install -r requirements.txt
```

### Training Custom Model
```bash
# 1. Prepare dataset di asr/dataset/
# 2. Open training notebook
jupyter notebook asr/training/asr_training.ipynb

# 3. Atau jalankan script
python asr/training/train_asr_cnn.py

# 4. Model akan disimpan di asr/model/model_asr.h5
```

### Running Tests
```bash
# Test ASR preprocessing
python -c "from asr import preprocess_bytes; print('ASR OK')"

# Test TTS generation
python -c "from tts import list_voices; print(list_voices())"

# Test full app
streamlit run app.py
```

---

## 🚀 Deployment

### Local Machine
```bash
streamlit run app.py
```
Akses di: `http://localhost:8501`

### Docker (Optional)
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

### Cloud Deployment (Streamlit Cloud)
1. Push code ke GitHub
2. Buka [streamlit.io/cloud](https://streamlit.io/cloud)
3. Deploy dari repository

---

## 📞 Support & Contact

**Issues atau pertanyaan?**
- Lihat documentation files di folder root
- Open GitHub issue untuk bug reports

---

## 📜 License

MIT License - Silakan gunakan dan modify sesuai kebutuhan

---

## 👥 Team

Proyek ini dikembangkan sebagai tugas akhir oleh:
- Matilde Ina Ola Dosinaeng
- Angelina Geronsiana Yudrikewati
- Asri Tanisha Rumapea
- Abdullah Luthfi (luthfikkc@gmail.com)
- Daniel Febrian Sijabat

---

**Last Updated:** May 23, 2026  
**Project Status:** ✅ Production-Ready (dengan 2 minor issues, see docs)  
**Python Version:** 3.8+
