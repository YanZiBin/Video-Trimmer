# Specification: Video Trimmer Tool

## 1. Overview
A Windows desktop application that allows users to trim a specific number of frames from the end of a video file. It provides a real-time preview of the new last frame and ensures lossless export using FFmpeg stream copy.

## 2. Technical Architecture

### 2.1 Technology Stack
- **Language**: Python 3.10+
- **GUI**: Tkinter (Standard Library)
- **Video Processing (Core)**: FFmpeg (via `subprocess` calls) for trimming.
- **Video Processing (Preview)**: OpenCV (`cv2`) for fast frame extraction.
- **Packaging**: PyInstaller for `.exe` generation.

### 2.2 Project Structure
```text
project_root/
├── src/
│   ├── main.py           # Entry point
│   ├── ui/
│   │   └── app_window.py # Tkinter Main Window
│   ├── core/
│   │   └── video.py      # VideoProcessor Logic (FFmpeg/OpenCV wrapper)
│   └── utils/
│       └── helpers.py    # Time conversion, validation utils
├── tests/                # Unit tests
├── requirements.txt
└── build_script.py       # PyInstaller configuration
```

## 3. Detailed Requirements

### 3.1 Core Logic (`src/core/video.py`)
- **Class `VideoProcessor`**:
    - `__init__(file_path)`: Initialize with video file.
    - `get_metadata()`: Returns dict with `total_frames`, `fps`, `duration`.
    - `get_frame_image(frame_index)`: Returns a PIL-compatible Image object of the specific frame using OpenCV.
    - `trim_video(frames_to_remove, output_path)`:
        - Calculates `new_duration = total_duration - (frames_to_remove / fps)`.
        - Executes FFmpeg command: `ffmpeg -i input.mp4 -t new_duration -c copy output.mp4`.
        - Captures stdout/stderr for error handling.

### 3.2 User Interface (`src/ui/app_window.py`)
- **Layout**: Vertical arrangement.
    1.  **File Selection**: Label, Entry (readonly), "Browse" Button.
    2.  **Info Panel**: Display `Total Frames`, `FPS`.
    3.  **Trim Controls**:
        -   Label: "Remove last N frames:"
        -   Entry: Integer only.
        -   Button: "Update Preview" (or auto-update on focus out/Enter key).
    4.  **Preview Area**: Canvas/Label displaying the image.
    5.  **Actions**: "Save Processed Video" Button.
- **Validation**:
    -   Prevent non-integer input.
    -   Prevent input > total frames.
    -   Show error popup (Tkinter messagebox) on invalid input.

### 3.3 Packaging
- **FFmpeg Dependency**:
    -   **Development**: Assume FFmpeg is in system PATH.
    -   **Distribution**: The `.exe` should ideally bundle `ffmpeg.exe` or expect it in the same folder. *Decision for MVP: Expect `ffmpeg.exe` in the same folder as the app to keep size smaller, or check system PATH.*

## 4. Workflows
1.  **Load**: User selects video -> App reads metadata -> Displays total frames -> Shows last frame of original video as default preview.
2.  **Adjust**: User enters `10` -> App calculates `target_frame = total - 10` -> App seeks and displays `target_frame`.
3.  **Save**: User clicks Save -> File Dialog -> App runs FFmpeg -> Shows "Success" popup.

## 5. Constraints
- **Lossless**: Must use `-c copy`. If the cut point is not on a keyframe, FFmpeg might seek to the nearest keyframe.
    - *Refinement*: For exact frame accuracy with `-c copy`, results may vary depending on GOP size.
    - *Decision*: We will use `-c copy` as requested. If precision is off by a few frames due to GOP, we will accept this trade-off for speed/quality, OR we can offer a "Re-encode" mode later. For now, stick to `-c copy` as per requirements.
