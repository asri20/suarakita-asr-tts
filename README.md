# 🎙️ SuaraKita — ASR & TTS Bahasa Indonesia

Aplikasi web berbasis **Streamlit** yang menggabungkan **Automatic Speech Recognition (ASR)** dan **Text-to-Speech (TTS)** untuk Bahasa Indonesia.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🎤 ASR | Prediksi 12 nama dari audio menggunakan CNN 1D + MFCC |
| 🔊 TTS | Konversi teks ke suara natural (edge-tts Neural ID) |
| 📊 Visualisasi | Grafik MFCC dan Confidence Score |
| 🔄 Integrasi | Hasil ASR otomatis diteruskan ke TTS |
| ⬇️ Download | Export audio TTS sebagai MP3 |

---

## 🏗️ Struktur Proyek

```
speech-app/
│
├── app.py                      # Aplikasi utama Streamlit
├── requirements.txt
├── README.md
│
├── asr/
│   ├── __init__.py
│   ├── preprocess.py           # Normalisasi, trim, pad audio
│   ├── feature_extraction.py   # Ekstraksi MFCC + visualisasi
│   ├── predict.py              # Inferensi model
│   ├── utils.py                # Load dataset, utilities
│   │
│   ├── dataset/                # 📁 Letakkan dataset di sini
│   │   ├── yesus/   (40-50 file .wav)
│   │   ├── simon/
│   │   ├── ... (12 folder nama)
│   │   └── maria/
│   │
│   ├── model/
│   │   └── model_asr.h5        # 🧠 Model hasil training
│   │
│   └── training/
│       └── asr_training.ipynb  # 📓 Notebook Google Colab
│
├── tts/
│   ├── __init__.py
│   ├── generate.py             # edge-tts wrapper
│   ├── voices.py               # Konfigurasi suara & kecepatan
│   └── audio_output/           # File MP3 yang dihasilkan
│
├── audio/                      # Rekaman audio sementara
└── assets/                     # Gambar dan aset lainnya
```

---

## 🚀 Cara Menjalankan

### 1. Clone Repositori
```bash
git clone https://github.com/[username]/speech-app.git
cd speech-app
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Training Model (Google Colab)
1. Buka `asr/training/asr_training.ipynb` di Google Colab
2. Upload dataset audio ke Google Drive
3. Jalankan semua cell
4. Download `model_asr.h5` dan letakkan di `asr/model/`

### 4. Jalankan Aplikasi
```bash
streamlit run app.py
```

---

## 🗂️ Dataset

**Format**: WAV, 16kHz, mono, durasi 1–2 detik  
**Target**: 40–50 audio per kata × 12 kata = 500–600 total audio

| Nama | Label |
|------|-------|
| Yesus | `yesus` |
| Simon | `simon` |
| Andreas | `andreas` |
| Yakobus | `yakobus` |
| Yohanes | `yohanes` |
| Filipus | `filipus` |
| Bartomeleus | `bartomeleus` |
| Tomas | `tomas` |
| Matius | `matius` |
| Tadeus | `tadeus` |
| Yudas | `yudas` |
| Maria | `maria` |

---

## 🧠 Arsitektur Model CNN 1D

```
Input: (batch, 32, 13)
  ↓ Conv1D(32) → BatchNorm → MaxPool → Dropout
  ↓ Conv1D(64) → BatchNorm → MaxPool → Dropout
  ↓ Conv1D(128) → BatchNorm → GlobalAvgPool
  ↓ Dense(256) → Dropout
  ↓ Dense(128) → Dropout
  ↓ Dense(12, softmax)
```

---

## 🔊 TTS — Suara yang Tersedia

| Voice ID | Gender | Deskripsi |
|----------|--------|-----------|
| `id-ID-GadisNeural` | ♀️ Perempuan | Suara wanita natural |
| `id-ID-ArdiNeural` | ♂️ Laki-laki | Suara pria natural |

---

## 🛠️ Teknologi

- **Frontend**: Streamlit
- **ASR**: TensorFlow/Keras, librosa, NumPy, scikit-learn
- **TTS**: edge-tts, asyncio
- **Training**: Google Colab (GPU T4)
- **VCS**: GitHub

---

## 👥 Tim Pengembang

Proyek ini dikembangkan sebagai tugas akhir oleh anggota kelompok.

---

## 📄 Lisensi

MIT License
