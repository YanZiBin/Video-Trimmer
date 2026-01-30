"""Debug script to test user's video with exact mode."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.video import VideoProcessor

# Test with user's video
video_path = r"C:\Users\YanZiBin\Downloads\2.mp4"
output_path = "tests/output/user_trim_exact.mp4"

print(f"Loading video: {video_path}")
processor = VideoProcessor(video_path)
metadata = processor.get_metadata()

print(f"Original video:")
print(f"  Total frames: {metadata['total_frames']}")
print(f"  FPS: {metadata['fps']}")
print(f"  Duration: {metadata['duration']:.4f}s")

frames_to_remove = 2
print(f"\nTrimming {frames_to_remove} frames with EXACT mode (re-encoding)...")

processor.trim_video(frames_to_remove, output_path, exact=True)
processor.close()

# Check output
print(f"\nChecking output: {output_path}")
output_processor = VideoProcessor(output_path)
output_metadata = output_processor.get_metadata()

print(f"Output video:")
print(f"  Total frames: {output_metadata['total_frames']}")
print(f"  FPS: {output_metadata['fps']}")
print(f"  Duration: {output_metadata['duration']:.4f}s")

diff = metadata['total_frames'] - output_metadata['total_frames']
print(f"\nActual frames removed: {diff}")
print(f"Expected: {frames_to_remove}")

if diff == frames_to_remove:
    print("SUCCESS!")
else:
    print(f"DIFFERENCE: {abs(diff - frames_to_remove)} frames")

output_processor.close()
