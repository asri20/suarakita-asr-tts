from pydub import AudioSegment
from pathlib import Path

# Folder dataset utama
DATASET_DIR = Path(r"E:\S1Informatika\PTU\suarakita-asr-tts\asr\dataset")

# Cari semua file m4a dan mp3 di semua subfolder
audio_files = list(DATASET_DIR.rglob("*.m4a")) + list(DATASET_DIR.rglob("*.mp3"))

print(f"Total file ditemukan: {len(audio_files)}")

for audio_path in audio_files:

    # Nama output wav
    wav_path = audio_path.with_suffix(".wav")

    try:
        # Ambil ekstensi file
        ext = audio_path.suffix.replace(".", "").lower()

        # Load audio sesuai format
        audio = AudioSegment.from_file(audio_path, format=ext)

        # Convert:
        # mono + 16000 Hz
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)

        # Export ke wav
        audio.export(wav_path, format="wav")

         # Hapus file asli
        audio_path.unlink()

        print(f"Berhasil convert: {wav_path}")

    except Exception as e:
        print(f"Gagal convert {audio_path}: {e}")

print("Selesai convert semua file.")