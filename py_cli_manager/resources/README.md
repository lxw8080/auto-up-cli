# Resources / 图标资源

此目录用于存放应用程序图标文件。

## 需要的图标文件

### Windows
- **文件名**: `icon.ico`
- **尺寸**: 包含 16x16, 32x32, 48x48, 256x256 等多种尺寸
- **制作工具**:
  - [GIMP](https://www.gimp.org/) (免费)
  - [IcoFX](https://icofx.ro/)
  - 在线工具: [ConvertICO](https://convertio.co/zh/png-ico/)

### macOS
- **文件名**: `icon.icns`
- **尺寸**: 包含 16x16, 32x32, 128x128, 256x256, 512x512, 1024x1024
- **制作工具**:
  - [Iconutil](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/OptimizingResolutionforOSX/ResolutionforOSX.html) (系统自带)
  - [Icon Slate](https://www.icnsbuilder.com/)
  - 在线工具: [CloudConvert](https://cloudconvert.com/png-to-icns)

### Linux / 通用
- **文件名**: `icon.png`
- **尺寸**: 512x512 或更高 (推荐 1024x1024)
- **格式**: PNG with transparency

## 快速创建图标

### 使用 AI 生成图标
可以在图像生成 AI (如 Midjourney, DALL-E, Stable Diffusion) 中使用以下提示词：

```
A modern minimalist robot icon, simple geometric design,
blue and white color scheme, transparent background,
app icon style, 1024x1024
```

### 转换工具

**PNG → ICO (Windows)**:
```bash
# 使用 ImageMagick
convert icon.png -define icon:auto-resize=256,48,32,16 icon.ico
```

**PNG → ICNS (macOS)**:
```bash
# 使用 iconutil (macOS)
mkdir icon.iconset
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset
```

## 当前状态

图标文件尚未添加。如需添加图标，请：

1. 创建或获取图标图像
2. 转换为对应平台格式
3. 将文件放置在 `resources/` 目录下
4. 确保文件名正确：
   - Windows: `icon.ico`
   - macOS: `icon.icns`
   - Linux: `icon.png`

**注意**: 如果图标文件不存在，打包脚本会自动跳过图标设置，不影响打包流程。
