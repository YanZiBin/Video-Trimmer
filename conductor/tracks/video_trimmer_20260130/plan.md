# Implementation Plan: Video Trimmer Tool

## Phase 1: Core Logic & Environment Setup
- [ ] Task: Initialize Project Environment
    - Create virtual environment.
    - Create `requirements.txt` with `opencv-python`, `pillow`, `pyinstaller`.
    - Install dependencies.
- [ ] Task: Implement `VideoProcessor` Class structure
    - Create `src/core/video.py`.
    - Implement `load_video` using OpenCV to get metadata (fps, count).
- [ ] Task: Implement Frame Extraction
    - Implement `get_frame_image(index)` in `VideoProcessor`.
    - **Test**: Write unit test to verify it returns a valid PIL image object from a sample video.
- [ ] Task: Implement Trimming Logic (FFmpeg wrapper)
    - Implement `trim_video(frames_to_remove, output_path)`.
    - Construct `ffmpeg` command using `subprocess`.
    - **Test**: Verify command string construction and execution on a dummy file.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Core Logic & Environment Setup' (Protocol in workflow.md)

## Phase 2: UI Development (Tkinter)
- [ ] Task: Build Main Window Layout
    - Create `src/ui/app_window.py`.
    - Setup File Selection frame (Entry + Button).
    - Setup Preview Area (Canvas/Label).
    - Setup Control Panel (Input Entry + Save Button).
- [ ] Task: Connect Logic to UI (Loading)
    - Bind "Browse" button to file dialog.
    - On file load, instantiate `VideoProcessor`, display metadata, and show last frame.
- [ ] Task: Connect Logic to UI (Previewing)
    - Bind Enter key or FocusOut on the Input Entry to trigger preview update.
    - Implement validation (Int only, max frames check).
- [ ] Task: Connect Logic to UI (Exporting)
    - Bind "Save" button to `trim_video`.
    - Add Success/Error message boxes.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: UI Development (Tkinter)' (Protocol in workflow.md)

## Phase 3: Packaging & Delivery
- [ ] Task: Prepare Build Script
    - Create `build.spec` or use `pyinstaller` command line.
    - Ensure `ffmpeg.exe` handling strategy is defined (e.g., placed alongside dist).
- [ ] Task: Build Executable
    - Run PyInstaller.
    - Verify `.exe` runs on a clean environment (or at least outside the IDE).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Packaging & Delivery' (Protocol in workflow.md)
