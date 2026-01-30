"""
Main application window for the Video Trimmer Tool.

This module provides the Tkinter-based GUI for:
- Video file selection
- Metadata display (frames, FPS)
- Frame preview with trim adjustment
- Video export functionality
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Optional

from PIL import Image, ImageTk

from src.core.video import VideoProcessor, VideoProcessorError


class AppWindow:
    """
    Main application window for the Video Trimmer Tool.
    
    Provides a native Windows-style GUI with video preview,
    trim controls, and export functionality.
    """
    
    # Window configuration
    WINDOW_TITLE = "视频帧裁剪工具"
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 600
    PREVIEW_MAX_WIDTH = 640
    PREVIEW_MAX_HEIGHT = 360
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the application window.
        
        Args:
            root: The Tkinter root window.
        """
        self.root = root
        self.video_processor: Optional[VideoProcessor] = None
        self.current_image: Optional[ImageTk.PhotoImage] = None
        self.current_pil_image: Optional[Image.Image] = None  # Store original PIL image for saving
        self.video_path: Optional[str] = None
        
        # Setup window
        self._setup_window()
        self._create_widgets()
        self._layout_widgets()
        
    def _setup_window(self) -> None:
        """Configure the main window properties."""
        self.root.title(self.WINDOW_TITLE)
        self.root.minsize(self.WINDOW_MIN_WIDTH, self.WINDOW_MIN_HEIGHT)
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.WINDOW_MIN_WIDTH) // 2
        y = (screen_height - self.WINDOW_MIN_HEIGHT) // 2
        self.root.geometry(f"{self.WINDOW_MIN_WIDTH}x{self.WINDOW_MIN_HEIGHT}+{x}+{y}")
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)  # Preview area should expand
        
    def _create_widgets(self) -> None:
        """Create all UI widgets."""
        # === Video Selection Frame ===
        self.file_frame = ttk.LabelFrame(self.root, text="视频选择", padding=10)
        
        self.path_var = tk.StringVar(value="请选择视频文件...")
        self.path_label = ttk.Label(
            self.file_frame, 
            textvariable=self.path_var,
            width=60,
            anchor="w"
        )
        self.browse_btn = ttk.Button(
            self.file_frame, 
            text="选择视频",
            command=self._on_browse_click
        )
        
        # === Video Info Frame ===
        self.info_frame = ttk.LabelFrame(self.root, text="视频信息", padding=10)
        
        self.total_frames_var = tk.StringVar(value="总帧数: --")
        self.fps_var = tk.StringVar(value="FPS: --")
        self.duration_var = tk.StringVar(value="时长: --")
        
        self.total_frames_label = ttk.Label(self.info_frame, textvariable=self.total_frames_var)
        self.fps_label = ttk.Label(self.info_frame, textvariable=self.fps_var)
        self.duration_label = ttk.Label(self.info_frame, textvariable=self.duration_var)
        
        # === Trim Settings Frame ===
        self.trim_frame = ttk.LabelFrame(self.root, text="剪辑设置", padding=10)
        
        self.trim_label = ttk.Label(self.trim_frame, text="要去掉的末尾帧数：")
        
        # Entry with validation for integers only
        self.frames_var = tk.StringVar(value="0")
        self.frames_var.trace_add("write", self._on_frames_changed)
        
        vcmd = (self.root.register(self._validate_number), '%P')
        self.frames_entry = ttk.Entry(
            self.trim_frame, 
            textvariable=self.frames_var,
            width=10,
            validate='key',
            validatecommand=vcmd
        )
        
        self.preview_btn = ttk.Button(
            self.trim_frame, 
            text="刷新预览",
            command=self._on_preview_click
        )
        
        self.preview_info_var = tk.StringVar(value="预览帧: --")
        self.preview_info_label = ttk.Label(self.trim_frame, textvariable=self.preview_info_var)
        
        # === Preview Frame ===
        self.preview_frame = ttk.LabelFrame(self.root, text="预览", padding=10)
        
        self.preview_canvas = tk.Canvas(
            self.preview_frame,
            width=self.PREVIEW_MAX_WIDTH,
            height=self.PREVIEW_MAX_HEIGHT,
            bg="#2d2d2d"
        )
        
        # Placeholder text
        self.preview_canvas.create_text(
            self.PREVIEW_MAX_WIDTH // 2,
            self.PREVIEW_MAX_HEIGHT // 2,
            text="请选择视频文件",
            fill="#888888",
            font=("Microsoft YaHei", 14),
            tags="placeholder"
        )
        
        # === Export Frame ===
        self.export_frame = ttk.Frame(self.root, padding=10)
        
        # Save preview image button
        self.save_preview_btn = ttk.Button(
            self.export_frame,
            text="保存当前预览图",
            command=self._on_save_preview_click
        )
        
        self.export_btn = ttk.Button(
            self.export_frame,
            text="保存剪辑后的视频",
            command=self._on_export_click
        )
        # Make export button larger
        self.export_btn.configure(style="Large.TButton")
        
        # Create custom style for large button
        style = ttk.Style()
        style.configure("Large.TButton", padding=(20, 10), font=("Microsoft YaHei", 11))
        
    def _layout_widgets(self) -> None:
        """Arrange all widgets using grid layout."""
        # File selection frame
        self.file_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.path_label.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.browse_btn.grid(row=0, column=1)
        self.file_frame.columnconfigure(0, weight=1)
        
        # Info frame
        self.info_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.total_frames_label.grid(row=0, column=0, padx=20)
        self.fps_label.grid(row=0, column=1, padx=20)
        self.duration_label.grid(row=0, column=2, padx=20)
        
        # Trim settings frame
        self.trim_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.trim_label.grid(row=0, column=0)
        self.frames_entry.grid(row=0, column=1, padx=5)
        self.preview_btn.grid(row=0, column=2, padx=10)
        self.preview_info_label.grid(row=0, column=3, padx=20)
        
        # Preview frame
        self.preview_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        self.preview_canvas.pack(expand=True)
        
        # Export frame
        self.export_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        self.save_preview_btn.pack(side="left", padx=(0, 20))
        self.export_btn.pack(side="left")
        
        # Initial button states
        self._set_controls_enabled(False)
        
    def _validate_number(self, value: str) -> bool:
        """
        Validate that input is a non-negative integer.
        
        Args:
            value: The input value to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        if value == "":
            return True
        try:
            int(value)
            return value.isdigit() or value == ""
        except ValueError:
            return False
            
    def _set_controls_enabled(self, enabled: bool) -> None:
        """
        Enable or disable controls that require a loaded video.
        
        Args:
            enabled: Whether to enable the controls.
        """
        state = "normal" if enabled else "disabled"
        self.frames_entry.configure(state=state)
        self.preview_btn.configure(state=state)
        self.save_preview_btn.configure(state=state)
        self.export_btn.configure(state=state)
        
    def _on_browse_click(self) -> None:
        """Handle browse button click - open file dialog."""
        filetypes = [
            ("视频文件", "*.mp4 *.avi *.mkv *.mov *.wmv"),
            ("MP4 文件", "*.mp4"),
            ("所有文件", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=filetypes
        )
        
        if filepath:
            self._load_video(filepath)
            
    def _load_video(self, filepath: str) -> None:
        """
        Load a video file and update the UI.
        
        Args:
            filepath: Path to the video file.
        """
        try:
            # Close existing processor if any
            if self.video_processor:
                self.video_processor.close()
                
            # Create new processor
            self.video_processor = VideoProcessor(filepath)
            self.video_path = filepath
            
            # Update UI with video info
            metadata = self.video_processor.get_metadata()
            
            self.path_var.set(filepath)
            self.total_frames_var.set(f"总帧数: {metadata['total_frames']}")
            self.fps_var.set(f"FPS: {metadata['fps']:.2f}")
            self.duration_var.set(f"时长: {metadata['duration']:.2f}秒")
            
            # Reset frames to remove
            self.frames_var.set("0")
            
            # Enable controls
            self._set_controls_enabled(True)
            
            # Show last frame as initial preview
            self._update_preview(0)
            
        except VideoProcessorError as e:
            messagebox.showerror("加载错误", f"无法加载视频文件:\n{e}")
        except Exception as e:
            messagebox.showerror("错误", f"发生未知错误:\n{e}")
            
    def _on_frames_changed(self, *args) -> None:
        """Handle changes to the frames entry (for real-time validation info)."""
        # Update preview info label
        if self.video_processor:
            try:
                frames_to_remove = int(self.frames_var.get() or "0")
                metadata = self.video_processor.get_metadata()
                target_index = metadata['total_frames'] - 1 - frames_to_remove
                
                if target_index >= 0:
                    self.preview_info_var.set(f"预览帧: {target_index}")
                else:
                    self.preview_info_var.set("预览帧: 无效")
            except ValueError:
                self.preview_info_var.set("预览帧: --")
                
    def _on_preview_click(self) -> None:
        """Handle preview button click - update preview image."""
        if not self.video_processor:
            return
            
        try:
            frames_to_remove = int(self.frames_var.get() or "0")
            self._update_preview(frames_to_remove)
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")
            
    def _update_preview(self, frames_to_remove: int) -> None:
        """
        Update the preview image based on frames to remove.
        
        Args:
            frames_to_remove: Number of frames to remove from end.
        """
        if not self.video_processor:
            return
            
        metadata = self.video_processor.get_metadata()
        total_frames = metadata['total_frames']
        
        # Calculate target frame index
        target_index = total_frames - 1 - frames_to_remove
        
        # Validate
        if frames_to_remove < 0:
            messagebox.showerror("输入错误", "帧数不能为负数")
            return
            
        if frames_to_remove >= total_frames:
            messagebox.showerror(
                "输入错误", 
                f"要去掉的帧数 ({frames_to_remove}) 不能大于等于总帧数 ({total_frames})"
            )
            return
            
        try:
            # Get frame image
            pil_image = self.video_processor.get_frame_image(target_index)
            
            # Store original PIL image for saving
            self.current_pil_image = pil_image.copy()
            
            # Resize to fit preview area while maintaining aspect ratio
            pil_image = self._resize_image(pil_image)
            
            # Convert to PhotoImage
            self.current_image = ImageTk.PhotoImage(pil_image)
            
            # Clear canvas and display new image
            self.preview_canvas.delete("all")
            
            # Center image on canvas
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            # Use configured size if canvas hasn't been displayed yet
            if canvas_width <= 1:
                canvas_width = self.PREVIEW_MAX_WIDTH
            if canvas_height <= 1:
                canvas_height = self.PREVIEW_MAX_HEIGHT
                
            x = canvas_width // 2
            y = canvas_height // 2
            
            self.preview_canvas.create_image(x, y, image=self.current_image, anchor="center")
            
            # Update preview info
            self.preview_info_var.set(f"预览帧: {target_index} / {total_frames - 1}")
            
        except VideoProcessorError as e:
            messagebox.showerror("预览错误", f"无法获取帧图像:\n{e}")
            
    def _resize_image(self, image: Image.Image) -> Image.Image:
        """
        Resize image to fit preview area while maintaining aspect ratio.
        
        Args:
            image: PIL Image to resize.
            
        Returns:
            PIL.Image.Image: Resized image.
        """
        # Calculate scaling factor
        width_ratio = self.PREVIEW_MAX_WIDTH / image.width
        height_ratio = self.PREVIEW_MAX_HEIGHT / image.height
        scale = min(width_ratio, height_ratio)
        
        # Only downscale, never upscale
        if scale < 1:
            new_width = int(image.width * scale)
            new_height = int(image.height * scale)
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        return image
        
    def _on_save_preview_click(self) -> None:
        """Handle save preview button click - save current preview image."""
        if not self.current_pil_image:
            messagebox.showwarning("提示", "没有可保存的预览图，请先加载视频")
            return
            
        # Generate default filename
        if self.video_path:
            original_path = Path(self.video_path)
            frames_to_remove = int(self.frames_var.get() or "0")
            metadata = self.video_processor.get_metadata()
            target_frame = metadata['total_frames'] - 1 - frames_to_remove
            default_name = f"{original_path.stem}_frame{target_frame}.png"
        else:
            default_name = "preview_frame.png"
            
        # Open save dialog
        output_path = filedialog.asksaveasfilename(
            title="保存预览图",
            initialfile=default_name,
            defaultextension=".png",
            filetypes=[
                ("PNG 图片", "*.png"),
                ("JPEG 图片", "*.jpg"),
                ("所有文件", "*.*")
            ]
        )
        
        if not output_path:
            return  # User cancelled
            
        try:
            # Save the original full-resolution image
            self.current_pil_image.save(output_path)
            messagebox.showinfo("保存成功", f"预览图已保存到:\n{output_path}")
        except Exception as e:
            messagebox.showerror("保存错误", f"无法保存图片:\n{e}")
        
    def _on_export_click(self) -> None:
        """Handle export button click - save trimmed video."""
        if not self.video_processor or not self.video_path:
            return
            
        try:
            frames_to_remove = int(self.frames_var.get() or "0")
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")
            return
            
        # Validate frames
        metadata = self.video_processor.get_metadata()
        total_frames = metadata['total_frames']
        
        if frames_to_remove <= 0:
            messagebox.showwarning("提示", "没有需要裁剪的帧，视频将保持原样")
            return
            
        if frames_to_remove >= total_frames:
            messagebox.showerror(
                "输入错误",
                f"要去掉的帧数 ({frames_to_remove}) 不能大于等于总帧数 ({total_frames})"
            )
            return
            
        # Generate default filename
        original_path = Path(self.video_path)
        default_name = f"{original_path.stem}_minus{frames_to_remove}{original_path.suffix}"
        
        # Open save dialog
        output_path = filedialog.asksaveasfilename(
            title="保存剪辑后的视频",
            initialfile=default_name,
            defaultextension=".mp4",
            filetypes=[
                ("MP4 文件", "*.mp4"),
                ("所有文件", "*.*")
            ]
        )
        
        if not output_path:
            return  # User cancelled
            
        try:
            # Disable UI during export
            self.export_btn.configure(state="disabled", text="处理中...")
            self.root.update()
            
            # Perform trim
            self.video_processor.trim_video(frames_to_remove, output_path)
            
            # Show success message
            messagebox.showinfo(
                "导出成功",
                f"视频已保存到:\n{output_path}\n\n"
                f"已移除 {frames_to_remove} 帧"
            )
            
        except VideoProcessorError as e:
            messagebox.showerror("导出错误", f"无法导出视频:\n{e}")
        except Exception as e:
            messagebox.showerror("错误", f"发生未知错误:\n{e}")
        finally:
            # Re-enable UI
            self.export_btn.configure(state="normal", text="保存剪辑后的视频")
            
    def cleanup(self) -> None:
        """Clean up resources when closing."""
        if self.video_processor:
            self.video_processor.close()
