# Building Standalone Executable

This document explains how to build a self-contained executable of the PDF Rasterizer that includes all dependencies.

## Prerequisites

1. Python 3.8+ with pip
2. Virtual environment (recommended)

## Build Process

### 1. Set up the environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Build the executable

```bash
# Clean build using the spec file
pyinstaller pdf_rasterizer.spec --clean
```

## Output Files

After building, you'll find these files in the `dist/` directory:

### macOS
- `pdf_rasterizer` - Command-line executable (33MB)
- `PDFRasterizer.app` - macOS application bundle

### Windows
- `pdf_rasterizer.exe` - Windows executable

### Linux
- `pdf_rasterizer` - Linux executable

## Distribution

The standalone executable:
- ✅ Includes all Python dependencies (PyMuPDF, Pillow)
- ✅ Includes Python interpreter
- ✅ Requires no additional installations
- ✅ Works on systems without Python
- ✅ Self-contained in a single file/bundle

## Usage

The standalone executable works exactly like the Python script:

```bash
# Basic usage
./dist/pdf_rasterizer document.pdf

# Create flattened PDF
./dist/pdf_rasterizer document.pdf --create-pdf

# High-quality JPEG output
./dist/pdf_rasterizer document.pdf --dpi 600 --format JPEG

# Get PDF info
./dist/pdf_rasterizer document.pdf --info
```

## File Sizes

Typical executable sizes:
- **macOS (ARM64)**: ~33MB
- **Windows**: ~35-40MB  
- **Linux**: ~30-35MB

The larger size is due to bundling:
- Python interpreter
- PyMuPDF library (includes MuPDF C library)
- Pillow library
- All Python standard library modules

## Deployment Notes

### macOS
- The `.app` bundle can be dragged to Applications folder
- Command-line executable can be placed anywhere in PATH
- May require allowing "unidentified developer" in Security settings

### Windows
- Executable may trigger antivirus warnings (false positive)
- Can be distributed as-is or wrapped in an installer

### Linux
- Make executable: `chmod +x pdf_rasterizer`
- Copy to `/usr/local/bin/` for system-wide access

## Cross-Platform Building

To build for different platforms:

1. **For Windows** (from macOS/Linux):
   ```bash
   # Use Docker or Windows VM
   pyinstaller --target-arch=x86_64 pdf_rasterizer.spec
   ```

2. **For Linux** (from macOS):
   ```bash
   # Use Docker
   docker run -v $(pwd):/app python:3.12 bash -c "cd /app && pip install -r requirements.txt pyinstaller && pyinstaller pdf_rasterizer.spec"
   ```

## Troubleshooting

### Common Issues

1. **Import errors**: Add missing modules to `hiddenimports` in the spec file
2. **Large file size**: Remove unnecessary modules in `excludes`
3. **Slow startup**: Normal for bundled executables, ~1-2 seconds
4. **Missing files**: Check warnings in build output

### Reducing File Size

Edit `pdf_rasterizer.spec` to exclude unused modules:

```python
excludes=[
    'tkinter',
    'unittest', 
    'test',
    'distutils',
]
```

### Platform-Specific Builds

The spec file includes platform detection:
- macOS: Creates both executable and .app bundle
- Windows: Creates .exe with console
- Linux: Creates standard executable

## Security Notes

- Executables are not code-signed by default
- May trigger security warnings on some systems
- Consider code signing for production distribution
- Scan with antivirus before distribution to avoid false positives 