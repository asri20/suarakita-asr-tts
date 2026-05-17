## Folder ini berisi model ASR yang sudah dilatih

Letakkan file `model_asr.h5` di folder ini setelah training selesai di Google Colab.

### Cara mendapatkan model:
1. Buka file `../training/asr_training.ipynb` di Google Colab
2. Upload dataset audio ke Google Drive
3. Jalankan seluruh cell training
4. Download file `model_asr.h5` dari Google Drive
5. Salin ke folder ini: `asr/model/model_asr.h5`

### Spesifikasi model:
- **Arsitektur**: CNN 1D (Conv1D + MaxPooling + Dense)
- **Input shape**: (32, 13) — 32 frames × 13 MFCC coefficients
- **Output**: 12 kelas (softmax)
- **Format**: HDF5 (.h5)
