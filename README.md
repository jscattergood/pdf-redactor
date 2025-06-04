# PDF Rasterizer

A Python script that converts PDF pages into high-quality raster images, ensuring that all text and vector elements are flattened into bitmap format. This tool is useful for creating image versions of PDFs that preserve the visual appearance while removing any selectable text or vector data.

## Features

- **High-quality rasterization** with customizable DPI settings
- **Multiple output formats** (PNG, JPEG, TIFF, BMP)
- **Image enhancement** options for better quality
- **Batch processing** of all pages in a PDF
- **PDF information extraction** 
- **Command-line interface** with extensive options
- **Detailed logging** and progress tracking

## Installation

### Option 1: Python Script
1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Standalone Executable
Download the pre-built executable from the releases page or build it yourself:
```bash
pip install pyinstaller
pyinstaller pdf_rasterizer.spec --clean
```
The executable will be created in the `dist/` directory and requires no additional installations.

See [BUILD.md](BUILD.md) for detailed build instructions.

## Dependencies

- **PyMuPDF (fitz)**: For PDF processing and rendering
- **Pillow (PIL)**: For image processing and format conversion
- **pathlib**: For cross-platform file path handling

## Usage

### Basic Usage

Convert a PDF to PNG images at 300 DPI (default):

```bash
python pdf_rasterizer.py document.pdf
```

### macOS Integration

**Right-click any PDF in Finder!** The tool can be integrated with macOS using Automator Quick Actions for convenient right-click access. See [macOS Integration Guide](macos_integration.md) for setup instructions.

- ✅ Right-click PDF → "Flatten PDF" 
- ✅ Right-click PDF → "Convert to Images"
- ✅ Works with multiple selected files
- ✅ Automatic notifications when complete

### Advanced Usage

```bash
# High-quality JPEG output at 600 DPI
python pdf_rasterizer.py document.pdf --dpi 600 --format JPEG

# Custom output directory and filename prefix
python pdf_rasterizer.py document.pdf --output-dir ./images --prefix "doc"

# Create a flattened PDF (all text/vectors rasterized)
python pdf_rasterizer.py document.pdf --create-pdf

# Create flattened PDF and keep individual images
python pdf_rasterizer.py document.pdf --create-pdf --keep-images

# Disable image enhancement
python pdf_rasterizer.py document.pdf --no-enhance

# Show PDF information without processing
python pdf_rasterizer.py document.pdf --info

# Verbose logging
python pdf_rasterizer.py document.pdf --verbose
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `input_pdf` | Path to the input PDF file (required) |
| `--dpi` | Resolution in DPI (default: 300) |
| `--format` | Output image format: PNG, JPEG, TIFF, BMP (default: PNG) |
| `--output-dir` | Output directory (default: same as input file) |
| `--prefix` | Filename prefix (default: input filename) |
| `--create-pdf` | Create a flattened PDF from rasterized images |
| `--keep-images` | Keep individual image files when creating PDF |
| `--no-enhance` | Disable image quality enhancement |
| `--info` | Show PDF information and exit |
| `--verbose, -v` | Enable verbose logging |

## Examples

### Example 1: Basic Rasterization
```bash
python pdf_rasterizer.py report.pdf
```
Output: `report_page_01.png`, `report_page_02.png`, etc.

### Example 2: High-Quality TIFF Output
```bash
python pdf_rasterizer.py presentation.pdf --dpi 600 --format TIFF --output-dir ./tiff_images
```

### Example 3: Create Flattened PDF
```bash
python pdf_rasterizer.py document.pdf --create-pdf
```
Output: `document_rasterized.pdf` (completely flattened, no selectable text)

### Example 4: PDF Information
```bash
python pdf_rasterizer.py document.pdf --info
```
Output:
```
PDF Information:
Title: Sample Document
Author: John Doe
Subject: None
Pages: 5

Page Details:
  Page 1: 612.0x792.0 pts (rotation: 0°)
  Page 2: 612.0x792.0 pts (rotation: 0°)
  ...
```

## Output Quality Settings

The script automatically applies optimal settings for each output format:

- **PNG**: Optimized compression with level 6
- **JPEG**: 95% quality, optimized, progressive
- **TIFF**: LZW compression with predictor
- **BMP**: Standard bitmap format

### Image Enhancement

By default, the script applies subtle enhancements:
- Slight contrast boost (1.1x)
- Slight sharpness enhancement (1.1x)

Use `--no-enhance` to disable these enhancements.

## DPI Recommendations

| Use Case | Recommended DPI |
|----------|-----------------|
| Web display | 150-200 |
| Print preview | 300 |
| High-quality print | 600 |
| Archive/OCR | 300-400 |

## Programmatic Usage

You can also use the `PDFRasterizer` class directly in your Python code:

```python
from pdf_rasterizer import PDFRasterizer

# Initialize rasterizer
rasterizer = PDFRasterizer(dpi=300, output_format='PNG')

# Get PDF information
info = rasterizer.get_pdf_info('document.pdf')
print(f"PDF has {info['page_count']} pages")

# Rasterize PDF
output_files = rasterizer.rasterize_pdf(
    input_path='document.pdf',
    output_dir='./images',
    filename_prefix='doc',
    enhance_quality=True
)

print(f"Generated {len(output_files)} images")
```

## Error Handling

The script includes comprehensive error handling:
- Validates input file existence
- Checks output format support
- Handles PDF parsing errors
- Continues processing if individual pages fail
- Provides detailed error messages

## Performance Notes

- Processing time depends on PDF complexity and DPI settings
- Higher DPI settings produce larger files and take longer to process
- Complex PDFs with many vector elements may take longer to rasterize
- Consider using JPEG format for smaller file sizes when quality permits

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure all dependencies are installed via `pip install -r requirements.txt`
2. **Permission Error**: Check file permissions for input PDF and output directory
3. **Memory Error**: Try reducing DPI for very large PDFs
4. **Corrupted PDF**: Use `--info` flag to check if PDF can be opened

### Getting Help

Run the script with `--help` to see all available options:

```bash
python pdf_rasterizer.py --help
```

## License

This script is provided as-is for educational and practical use. Feel free to modify and adapt it to your needs. 

## PDF Flattening Feature

The `--create-pdf` option creates a new PDF file where each page is a rasterized image. This is useful for:
- **Removing selectable text** while preserving visual appearance
- **Flattening vector graphics** into bitmap images
- **Creating "print-ready" documents** that display consistently
- **Document redaction** where text needs to be completely removed

The flattened PDF will:
- Look identical to the original
- Have no selectable or searchable text
- Contain only rasterized images as pages
- Maintain the original page dimensions and aspect ratios 