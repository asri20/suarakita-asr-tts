"""
TTS Module - Text-to-Speech Bahasa Indonesia menggunakan edge-tts
"""

from .generate import generate_speech, generate_speech_bytes, list_available_voices, clean_old_audio
from .voices import (
    VOICES, SPEED_OPTIONS, VOLUME_OPTIONS,
    get_voice_id, get_speed_value, get_volume_value,
    list_voices, list_speeds, list_volumes,
    DEFAULT_VOICE, DEFAULT_SPEED,
)

__all__ = [
    "generate_speech", "generate_speech_bytes",
    "list_available_voices", "clean_old_audio",
    "VOICES", "SPEED_OPTIONS", "VOLUME_OPTIONS",
    "get_voice_id", "get_speed_value", "get_volume_value",
    "list_voices", "list_speeds", "list_volumes",
    "DEFAULT_VOICE", "DEFAULT_SPEED",
]
