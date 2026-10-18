"""Compatibility runner for the current native room-view presentation."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("test_room_view_review.py")),run_name="__main__")
