#!/usr/bin/env python3
"""
export_mfcc.py - Export semua MFCC features dari dataset ke CSV
Jalankan: python asr/export_mfcc.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from asr.feature_extraction import export_mfcc_to_csv


if __name__ == "__main__":
    try:
        export_mfcc_to_csv()
        print("\n✨ Semua MFCC features sudah di-export ke CSV!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
