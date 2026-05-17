"""
voices.py - Konfigurasi suara multilingual untuk edge-tts
"""

# ─────────────────────────────────────────────────────────────
# Voice multilingual
# ─────────────────────────────────────────────────────────────

VOICES = {

    # INDONESIA
    "Indonesia — Perempuan (Gadis)": "id-ID-GadisNeural",
    "Indonesia — Laki-laki (Ardi)": "id-ID-ArdiNeural",

    # ENGLISH
    "English — Female (Jenny)": "en-US-JennyNeural",
    "English — Male (Guy)": "en-US-GuyNeural",

    # JAPANESE
    "Japanese — Female (Nanami)": "ja-JP-NanamiNeural",
    "Japanese — Male (Keita)": "ja-JP-KeitaNeural",

    # KOREAN
    "Korean — Female (SunHi)": "ko-KR-SunHiNeural",
    "Korean — Male (InJoon)": "ko-KR-InJoonNeural",
}

# ─────────────────────────────────────────────────────────────
# Kecepatan bicara
# ─────────────────────────────────────────────────────────────

SPEED_OPTIONS = {
    "Lambat": "-20%",
    "Normal": "+0%",
    "Cepat": "+25%",
    "Sangat Cepat": "+50%",
}

# ─────────────────────────────────────────────────────────────
# Volume
# ─────────────────────────────────────────────────────────────

VOLUME_OPTIONS = {
    "Pelan": "-20%",
    "Normal": "+0%",
    "Keras": "+20%",
}

# ─────────────────────────────────────────────────────────────
# Default settings
# ─────────────────────────────────────────────────────────────

DEFAULT_VOICE = "id-ID-GadisNeural"
DEFAULT_SPEED = "+0%"
DEFAULT_VOLUME = "+0%"

# ─────────────────────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────────────────────

def get_voice_id(display_name: str) -> str:
    """Dapatkan ID voice dari display name."""
    return VOICES.get(display_name, DEFAULT_VOICE)


def get_speed_value(display_name: str) -> str:
    """Dapatkan nilai speed."""
    return SPEED_OPTIONS.get(display_name, DEFAULT_SPEED)


def get_volume_value(display_name: str) -> str:
    """Dapatkan nilai volume."""
    return VOLUME_OPTIONS.get(display_name, DEFAULT_VOLUME)


def list_voices() -> list:
    """List semua voice."""
    return list(VOICES.keys())


def list_speeds() -> list:
    """List speed."""
    return list(SPEED_OPTIONS.keys())


def list_volumes() -> list:
    """List volume."""
    return list(VOLUME_OPTIONS.keys())