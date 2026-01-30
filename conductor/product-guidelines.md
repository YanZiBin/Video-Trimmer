# Product Guidelines

## Visual Identity
- **Style**: 原生 Windows 窗口风格。
- **UI Framework**: Tkinter (Python 标准库)，确保在 Windows 上有最稳定的原生表现。
- **Layout**: 简洁垂直布局。顶部为文件选择区，中间为输入和预览区，底部为操作按钮区。

## Interaction Design
- **Input Validation**: 
  - 仅允许输入正整数。
  - 实时监听输入，但预览图更新建议增加一个“确认/刷新预览”按钮，避免输入过程中的频繁卡顿。
- **Error Handling**: 
  - 当输入非数字、负数或超过视频总帧数时，弹出标准 Windows 错误对话框提示用户。
  - 文件读取失败或保存失败时，提供详细的弹窗提示。

## Content Guidelines
- **Export Naming**: 默认建议文件名为 `{original_name}_minus{frames}.{ext}`。
- **Language**: 界面文本使用简体中文。

## Technical Requirements
- **Performance**: 预览图提取需在 1 秒内完成。
- **Reliability**: 视频导出必须采用无损（Stream Copy）模式，以确保与原视频参数完全一致。
