from pathlib import Path

DATASET_DIR = Path(r"E:\S1Informatika\PTU\Dataset - Copy")

wav_files = list(DATASET_DIR.rglob("*.wav"))

print(f"Total file .wav ditemukan: {len(wav_files)}")
for file in wav_files:
    print(file)

confirm = input("Yakin hapus semua file .wav? ketik YES: ")

if confirm == "YES":
    for file in wav_files:
        file.unlink()
    print("Semua file .wav berhasil dihapus.")
else:
    print("Dibatalkan.")