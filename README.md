# Video Trimmer / 视频剪辑工具

一款轻量级的桌面端视频剪辑工具，专为优化 AI 图生视频工作流而设计。通过精准剪除视频尾部帧，解决生成视频末尾帧质量不佳的问题。

A lightweight desktop video trimming tool designed to optimize the AI image-to-video workflow. It solves the problem of poor-quality frames at the end of generated videos by precisely trimming frames from the end.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

---

## ✨ 功能特性 / Features

- 🎬 **视频导入 / Video Import** - 支持主流视频格式 (MP4, AVI, MKV, MOV, WMV) / Supports mainstream video formats
- ✂️ **精准剪辑 / Precise Trimming** - 直接输入需要去掉的末尾帧数 / Directly input the number of frames to remove from the end
- 👁️ **即时预览 / Real-time Preview** - 实时显示处理后的最后一帧静态图片 / Real-time display of the last frame after processing
- 🚀 **无损输出 / Lossless Output** - 保持原视频的格式、编码、码率等所有参数 / Maintains all original video parameters (format, codec, bitrate, etc.)
- 💾 **灵活保存 / Flexible Saving** - 手动选择输出路径和文件名 / Manually select output path and filename

---

## 📦 安装 / Installation

### 方法一：下载可执行文件 / Option 1: Download Executable

从 [Releases](https://github.com/YanZiBin/video-trimmer/releases) 页面下载最新的 `.exe` 文件，双击即可运行。

Download the latest `.exe` file from the [Releases](https://github.com/YanZiBin/video-trimmer/releases) page and double-click to run.

### 方法二：源码运行 / Option 2: Run from Source

#### 环境要求 / Requirements

- Python 3.9+
- FFmpeg

#### 安装步骤 / Installation Steps

1. 克隆仓库 / Clone the repository
```bash
git clone https://github.com/YanZiBin/video-trimmer.git
cd video-trimmer
```

2. 安装依赖 / Install dependencies
```bash
pip install -r requirements.txt
```

3. 下载 FFmpeg / Download FFmpeg
- Windows 用户：下载 [ffmpeg.exe](https://github.com/BtbN/FFmpeg-Builds/releases) 并放到项目根目录
- Windows users: Download [ffmpeg.exe](https://github.com/BtbN/FFmpeg-Builds/releases) and place it in the project root directory
- 或者将 FFmpeg 添加到系统 PATH / Or add FFmpeg to your system PATH

4. 运行程序 / Run the application
```bash
python src/main.py
```

---

## 🚀 使用方法 / Usage

1. **选择视频 / Select Video** - 点击"选择视频"按钮导入视频文件 / Click "Select Video" button to import a video file
2. **查看信息 / View Info** - 自动显示视频总帧数、FPS 和时长 / Automatically displays total frames, FPS, and duration
3. **调整帧数 / Adjust Frames** - 输入要去掉的末尾帧数 / Enter the number of frames to remove from the end
4. **预览效果 / Preview** - 点击"刷新预览"查看剪辑后的最后一帧 / Click "Refresh Preview" to view the last frame after trimming
5. **保存视频 / Save Video** - 满意后点击"保存剪辑后的视频" / Click "Save Trimmed Video" when satisfied

---

## 📁 项目结构 / Project Structure

```
video-trimmer/
├── src/
│   ├── main.py              # 主入口 / Main entry point
│   ├── core/
│   │   └── video.py         # 视频处理核心逻辑 / Video processing core logic
│   └── ui/
│       └── app_window.py    # GUI 界面 / GUI interface
├── tests/                   # 测试文件 / Test files
├── requirements.txt         # Python 依赖 / Python dependencies
├── VideoTrimmer.spec        # PyInstaller 打包配置 / PyInstaller build configuration
└── README.md                # 项目说明 / Project documentation
```

---

## 🛠️ 打包为可执行文件 / Build as Executable

```bash
pyinstaller VideoTrimmer.spec
```

打包完成后，可在 `dist/` 目录找到 `VideoTrimmer.exe`。

After building, you can find `VideoTrimmer.exe` in the `dist/` directory.

---

## 📝 技术栈 / Tech Stack

- **GUI 框架 / GUI Framework**: Tkinter
- **视频处理 / Video Processing**: OpenCV (cv2)
- **图像处理 / Image Processing**: Pillow
- **视频编码 / Video Encoding**: FFmpeg
- **打包工具 / Packaging Tool**: PyInstaller

---

## 📄 许可证 / License

本项目采用 [MIT 许可证](LICENSE)

This project is licensed under the [MIT License](LICENSE)

---

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

Issues and Pull Requests are welcome!

---

## 📧 联系方式 / Contact

如有问题或建议，请在 GitHub Issues 中反馈。

For questions or suggestions, please open an issue on GitHub.
