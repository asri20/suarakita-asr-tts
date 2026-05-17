"""
generate.py - Modul Text-to-Speech menggunakan edge-tts
Mendukung berbagai suara, kecepatan, dan volume Bahasa Indonesia
"""

import asyncio
import os
import tempfile
import time
from pathlib import Path
from typing import Optional

import edge_tts

from .voices import DEFAULT_VOICE, DEFAULT_SPEED, DEFAULT_VOLUME

# Folder output audio
OUTPUT_DIR = Path(__file__).parent / "audio_output"
OUTPUT_DIR.mkdir(exist_ok=True)


async def _generate_speech_async(
    text: str,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_SPEED,
    volume: str = DEFAULT_VOLUME,
    output_path: Optional[str] = None,
) -> str:
    """
    Generate speech secara async menggunakan edge-tts.
    
    Args:
        text: Teks yang akan diucapkan
        voice: ID suara edge-tts (contoh: "id-ID-GadisNeural")
        rate: Kecepatan bicara (contoh: "+0%", "+25%", "-20%")
        volume: Volume suara (contoh: "+0%", "+20%")
        output_path: Path output file MP3 (auto-generate jika None)
    
    Returns:
        Path file MP3 yang dihasilkan
    """
    if not text.strip():
        raise ValueError("Teks tidak boleh kosong!")

    if output_path is None:
        timestamp = int(time.time() * 1000)
        output_path = str(OUTPUT_DIR / f"tts_{timestamp}.mp3")

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume,
    )
    await communicate.save(output_path)
    return output_path


def generate_speech(
    text: str,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_SPEED,
    volume: str = DEFAULT_VOLUME,
    output_path: Optional[str] = None,
) -> str:
    """
    Generate speech synchronous wrapper.
    
    Returns:
        Path ke file MP3 yang dihasilkan
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(
        _generate_speech_async(text, voice, rate, volume, output_path)
    )


def generate_speech_bytes(
    text: str,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_SPEED,
    volume: str = DEFAULT_VOLUME,
) -> bytes:
    """
    Generate speech dan kembalikan sebagai bytes (untuk Streamlit st.audio).
    
    Returns:
        Audio bytes (MP3 format)
    """
    # Simpan ke temp file, baca, hapus
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        generate_speech(text, voice, rate, volume, output_path=tmp_path)
        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    return audio_bytes


async def _list_voices_async():
    """Dapatkan semua suara yang tersedia dari edge-tts."""
    voices = await edge_tts.list_voices()
    return [v for v in voices if v["Locale"].startswith("id-")]


def list_available_voices() -> list:
    """Kembalikan daftar suara Indonesia yang tersedia."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(_list_voices_async())
    except Exception:
        return []


def clean_old_audio(max_files: int = 20) -> None:
    """Bersihkan file audio lama di folder output."""
    files = sorted(OUTPUT_DIR.glob("tts_*.mp3"), key=os.path.getmtime)
    while len(files) > max_files:
        files.pop(0).unlink(missing_ok=True)
