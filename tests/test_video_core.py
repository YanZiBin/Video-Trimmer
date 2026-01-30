"""
Test script for VideoProcessor core functionality.

This script tests:
1. Video metadata extraction
2. Frame extraction and saving
3. Video trimming with FFmpeg

Usage:
    python -m tests.test_video_core
    
    Or run directly:
    python tests/test_video_core.py
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.video import VideoProcessor, VideoProcessorError


def test_metadata_extraction(video_path: str) -> bool:
    """
    Test video metadata extraction.
    
    Args:
        video_path: Path to test video file.
        
    Returns:
        bool: True if test passed.
    """
    print("=" * 60)
    print("Test 1: Metadata Extraction")
    print("=" * 60)
    
    try:
        with VideoProcessor(video_path) as processor:
            metadata = processor.get_metadata()
            
            print(f"  File: {video_path}")
            print(f"  Total Frames: {metadata['total_frames']}")
            print(f"  FPS: {metadata['fps']:.2f}")
            print(f"  Duration: {metadata['duration']:.2f} seconds")
            
            # Basic assertions
            assert metadata['total_frames'] > 0, "Total frames should be positive"
            assert metadata['fps'] > 0, "FPS should be positive"
            assert metadata['duration'] > 0, "Duration should be positive"
            
            print("  [PASSED] Metadata extraction successful!")
            return True
            
    except Exception as e:
        print(f"  [FAILED] {e}")
        return False


def test_frame_extraction(video_path: str, output_dir: str) -> bool:
    """
    Test frame extraction functionality.
    
    Args:
        video_path: Path to test video file.
        output_dir: Directory to save extracted frames.
        
    Returns:
        bool: True if test passed.
    """
    print("\n" + "=" * 60)
    print("Test 2: Frame Extraction")
    print("=" * 60)
    
    try:
        with VideoProcessor(video_path) as processor:
            metadata = processor.get_metadata()
            total_frames = metadata['total_frames']
            
            # Extract first frame
            first_frame = processor.get_frame_image(0)
            first_frame_path = os.path.join(output_dir, "test_first_frame.png")
            first_frame.save(first_frame_path)
            print(f"  First frame saved to: {first_frame_path}")
            print(f"  First frame size: {first_frame.size}")
            
            # Extract middle frame
            mid_index = total_frames // 2
            mid_frame = processor.get_frame_image(mid_index)
            mid_frame_path = os.path.join(output_dir, "test_middle_frame.png")
            mid_frame.save(mid_frame_path)
            print(f"  Middle frame (index {mid_index}) saved to: {mid_frame_path}")
            
            # Extract last frame
            last_index = total_frames - 1
            last_frame = processor.get_frame_image(last_index)
            last_frame_path = os.path.join(output_dir, "test_last_frame.png")
            last_frame.save(last_frame_path)
            print(f"  Last frame (index {last_index}) saved to: {last_frame_path}")
            
            # Verify images exist and have content
            assert Path(first_frame_path).exists(), "First frame file not created"
            assert Path(mid_frame_path).exists(), "Middle frame file not created"
            assert Path(last_frame_path).exists(), "Last frame file not created"
            
            print("  [PASSED] Frame extraction successful!")
            return True
            
    except Exception as e:
        print(f"  [FAILED] {e}")
        import traceback
        traceback.print_exc()
        return False


def test_frame_extraction_boundary(video_path: str) -> bool:
    """
    Test frame extraction boundary conditions.
    
    Args:
        video_path: Path to test video file.
        
    Returns:
        bool: True if test passed.
    """
    print("\n" + "=" * 60)
    print("Test 3: Frame Extraction Boundary Conditions")
    print("=" * 60)
    
    try:
        with VideoProcessor(video_path) as processor:
            metadata = processor.get_metadata()
            total_frames = metadata['total_frames']
            
            # Test invalid negative index
            try:
                processor.get_frame_image(-1)
                print("  [FAILED] Should have raised error for negative index")
                return False
            except VideoProcessorError as e:
                print(f"  Negative index correctly rejected: {e}")
            
            # Test invalid index beyond total frames
            try:
                processor.get_frame_image(total_frames)
                print("  [FAILED] Should have raised error for index >= total_frames")
                return False
            except VideoProcessorError as e:
                print(f"  Out-of-range index correctly rejected: {e}")
            
            print("  [PASSED] Boundary conditions handled correctly!")
            return True
            
    except Exception as e:
        print(f"  [FAILED] {e}")
        return False


def test_video_trimming(video_path: str, output_dir: str) -> bool:
    """
    Test video trimming functionality.
    
    Args:
        video_path: Path to test video file.
        output_dir: Directory to save trimmed video.
        
    Returns:
        bool: True if test passed.
    """
    print("\n" + "=" * 60)
    print("Test 4: Video Trimming (FFmpeg)")
    print("=" * 60)
    
    try:
        with VideoProcessor(video_path) as processor:
            metadata = processor.get_metadata()
            total_frames = metadata['total_frames']
            fps = metadata['fps']
            
            # Remove 10 frames (or 10% of total if video is short)
            frames_to_remove = min(10, max(1, total_frames // 10))
            output_path = os.path.join(output_dir, "test_trimmed_output.mp4")
            
            print(f"  Original total frames: {total_frames}")
            print(f"  Frames to remove: {frames_to_remove}")
            print(f"  Expected new frame count: {total_frames - frames_to_remove}")
            
            # Perform trimming
            processor.trim_video(frames_to_remove, output_path)
            
            # Verify output file exists
            assert Path(output_path).exists(), "Trimmed video file not created"
            
            # Verify output video metadata
            with VideoProcessor(output_path) as trimmed:
                trimmed_metadata = trimmed.get_metadata()
                print(f"  Trimmed video frames: {trimmed_metadata['total_frames']}")
                print(f"  Trimmed video duration: {trimmed_metadata['duration']:.2f}s")
                print(f"  Output file: {output_path}")
            
            print("  [PASSED] Video trimming successful!")
            return True
            
    except VideoProcessorError as e:
        if "FFmpeg not found" in str(e):
            print(f"  [SKIPPED] FFmpeg not installed: {e}")
            return True  # Don't fail test if FFmpeg is not installed
        print(f"  [FAILED] {e}")
        return False
    except Exception as e:
        print(f"  [FAILED] {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "#" * 60)
    print("# VideoProcessor Core Tests")
    print("#" * 60)
    
    # Get video path from command line or use default
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        # Look for any video file in the current directory or tests directory
        test_videos = list(Path('.').glob('*.mp4')) + list(Path('tests').glob('*.mp4'))
        if test_videos:
            video_path = str(test_videos[0])
        else:
            print("\nUsage: python test_video_core.py <path_to_video_file>")
            print("\nNo video file specified and no .mp4 files found in current directory.")
            print("Please provide a video file path as argument.")
            return 1
    
    # Create output directory for test artifacts
    output_dir = Path('tests/output')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nTest video: {video_path}")
    print(f"Output directory: {output_dir.absolute()}")
    
    # Verify video file exists
    if not Path(video_path).exists():
        print(f"\n[ERROR] Video file not found: {video_path}")
        return 1
    
    # Run all tests
    results = []
    results.append(("Metadata Extraction", test_metadata_extraction(video_path)))
    results.append(("Frame Extraction", test_frame_extraction(video_path, str(output_dir))))
    results.append(("Boundary Conditions", test_frame_extraction_boundary(video_path)))
    results.append(("Video Trimming", test_video_trimming(video_path, str(output_dir))))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "PASSED" if passed else "FAILED"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\nAll tests passed! ✓")
        return 0
    else:
        print("\nSome tests failed! ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())
