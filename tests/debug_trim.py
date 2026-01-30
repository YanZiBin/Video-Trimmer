"""Debug script to test FFmpeg trimming."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.video import VideoProcessor

# Test with test video
video_path = "tests/test_video.mp4"
output_path = "tests/output/debug_trim.mp4"

print(f"Loading video: {video_path}")
processor = VideoProcessor(video_path)
metadata = processor.get_metadata()

print(f"Original video:")
print(f"  Total frames: {metadata['total_frames']}")
print(f"  FPS: {metadata['fps']}")
print(f"  Duration: {metadata['duration']:.4f}s")

frames_to_remove = 30
new_frame_count = metadata['total_frames'] - frames_to_remove
new_duration = new_frame_count / metadata['fps']

print(f"\nTrimming {frames_to_remove} frames...")
print(f"  Expected new frame count: {new_frame_count}")
print(f"  Expected new duration: {new_duration:.4f}s")

processor.trim_video(frames_to_remove, output_path)
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

output_processor.close()
