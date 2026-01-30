"""
Video processing module for the Video Trimmer Tool.

This module provides the VideoProcessor class which handles:
- Video metadata extraction using OpenCV
- Frame extraction for preview
- Video trimming using FFmpeg subprocess calls
"""

import subprocess
import shutil
import sys
from pathlib import Path
from typing import Optional

import cv2
from PIL import Image


def get_ffmpeg_path() -> str:
    """
    Find the FFmpeg executable path.
    
    Checks in order:
    1. Same directory as the executable (for packaged app)
    2. Same directory as main script
    3. System PATH
    
    Returns:
        str: Path to ffmpeg executable.
        
    Raises:
        FileNotFoundError: If FFmpeg is not found.
    """
    # Check if running as packaged exe
    if getattr(sys, 'frozen', False):
        # Running as compiled
        app_dir = Path(sys.executable).parent
    else:
        # Running as script
        app_dir = Path(__file__).parent.parent.parent
    
    # Check for ffmpeg.exe in app directory
    ffmpeg_local = app_dir / 'ffmpeg.exe'
    if ffmpeg_local.exists():
        return str(ffmpeg_local)
    
    # Check system PATH
    ffmpeg_system = shutil.which('ffmpeg')
    if ffmpeg_system:
        return ffmpeg_system
    
    # Not found
    raise FileNotFoundError(
        "FFmpeg not found. Please ensure:\n"
        "1. Place ffmpeg.exe in the same folder as this application, OR\n"
        "2. Add FFmpeg to your system PATH"
    )


class VideoProcessorError(Exception):
    """Custom exception for video processing errors."""
    pass


class VideoProcessor:
    """
    A class to process video files for trimming operations.
    
    Uses OpenCV for metadata extraction and frame reading,
    and FFmpeg subprocess calls for lossless video trimming.
    """
    
    def __init__(self, file_path: str) -> None:
        """
        Initialize VideoProcessor with a video file.
        
        Args:
            file_path: Path to the video file to process.
            
        Raises:
            VideoProcessorError: If the video file cannot be opened.
        """
        self.file_path = file_path
        self._cap: Optional[cv2.VideoCapture] = None
        self._metadata: Optional[dict] = None
        
        # Validate and open the video file
        if not Path(file_path).exists():
            raise VideoProcessorError(f"Video file not found: {file_path}")
        
        self._cap = cv2.VideoCapture(file_path)
        if not self._cap.isOpened():
            raise VideoProcessorError(f"Cannot open video file: {file_path}")
        
        # Cache metadata on initialization
        self._metadata = self._extract_metadata()
    
    def _extract_metadata(self) -> dict:
        """
        Extract metadata from the video file.
        
        Returns:
            dict: Contains 'total_frames', 'fps', and 'duration'.
        """
        total_frames = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = self._cap.get(cv2.CAP_PROP_FPS)
        
        # Calculate duration in seconds
        duration = total_frames / fps if fps > 0 else 0.0
        
        return {
            'total_frames': total_frames,
            'fps': fps,
            'duration': duration
        }
    
    def get_metadata(self) -> dict:
        """
        Get video metadata.
        
        Returns:
            dict: Contains 'total_frames', 'fps', and 'duration'.
        """
        return self._metadata.copy()
    
    def get_frame_image(self, frame_index: int) -> Image.Image:
        """
        Extract a specific frame from the video as a PIL Image.
        
        Args:
            frame_index: The zero-based index of the frame to extract.
            
        Returns:
            PIL.Image.Image: The extracted frame as an RGB image.
            
        Raises:
            VideoProcessorError: If frame extraction fails or index is out of range.
        """
        total_frames = self._metadata['total_frames']
        
        # Validate frame index
        if frame_index < 0 or frame_index >= total_frames:
            raise VideoProcessorError(
                f"Frame index {frame_index} out of range [0, {total_frames - 1}]"
            )
        
        # Seek to the specified frame
        self._cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        
        # Read the frame
        ret, frame = self._cap.read()
        if not ret or frame is None:
            raise VideoProcessorError(f"Failed to read frame at index {frame_index}")
        
        # Convert from BGR (OpenCV format) to RGB (PIL format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(frame_rgb)
        
        return pil_image
    
    def trim_video(self, frames_to_remove: int, output_path: str, exact: bool = True) -> None:
        """
        Trim the video by removing frames from the end.
        
        Args:
            frames_to_remove: Number of frames to remove from the end.
            output_path: Path where the trimmed video will be saved.
            exact: If True, use re-encoding for frame-accurate trimming.
                   If False, use stream copy (faster but may not be exact due to keyframes).
            
        Raises:
            VideoProcessorError: If trimming fails or parameters are invalid.
        """
        total_frames = self._metadata['total_frames']
        fps = self._metadata['fps']
        
        # Validate frames_to_remove
        if frames_to_remove < 0:
            raise VideoProcessorError("frames_to_remove must be non-negative")
        if frames_to_remove >= total_frames:
            raise VideoProcessorError(
                f"Cannot remove {frames_to_remove} frames from video with {total_frames} frames"
            )
        
        # Calculate new duration in seconds
        new_frame_count = total_frames - frames_to_remove
        new_duration_seconds = new_frame_count / fps
        
        # Get FFmpeg path
        try:
            ffmpeg_path = get_ffmpeg_path()
        except FileNotFoundError as e:
            raise VideoProcessorError(str(e))
        
        # Build FFmpeg command
        if exact:
            # Re-encode for frame-accurate trimming
            # Use H.264 with high compatibility settings for Windows
            cmd = [
                ffmpeg_path, '-y',
                '-i', self.file_path,
                '-t', f'{new_duration_seconds:.6f}',
                '-c:v', 'libx264',         # H.264 video codec
                '-profile:v', 'main',      # Main profile for compatibility
                '-level', '4.0',           # Level 4.0 for broad compatibility
                '-pix_fmt', 'yuv420p',     # Pixel format for Windows compatibility
                '-preset', 'fast',         # Encoding speed/quality tradeoff
                '-crf', '18',              # High quality (lower = better)
                '-c:a', 'aac',             # AAC audio codec
                '-b:a', '192k',            # Audio bitrate
                '-movflags', '+faststart', # Enable fast start for streaming
                output_path
            ]
        else:
            # Stream copy (fast but keyframe-aligned only)
            cmd = [
                ffmpeg_path, '-y',
                '-i', self.file_path,
                '-to', f'{new_duration_seconds:.6f}',
                '-c', 'copy',
                '-avoid_negative_ts', 'make_zero',
                output_path
            ]
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            raise VideoProcessorError(f"FFmpeg error: {error_msg}")
        except FileNotFoundError:
            raise VideoProcessorError(
                "FFmpeg not found. Please ensure FFmpeg is installed and in your system PATH."
            )
    
    def close(self) -> None:
        """Release video capture resources."""
        if self._cap is not None:
            self._cap.release()
            self._cap = None
    
    def __enter__(self) -> 'VideoProcessor':
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - release resources."""
        self.close()
    
    def __del__(self) -> None:
        """Destructor - ensure resources are released."""
        self.close()
