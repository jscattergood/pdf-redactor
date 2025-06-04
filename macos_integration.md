# macOS Integration - Quick Actions

This guide shows how to integrate the PDF Rasterizer with macOS Finder using Automator Quick Actions, allowing you to right-click PDFs and process them directly.

## Overview

Automator Quick Actions (formerly called Services) appear in the right-click context menu and Finder's Services menu, providing convenient access to the PDF Rasterizer without using the command line.

## Setup Instructions

### Prerequisites
- Built executable in `dist/pdf_rasterizer` (see [BUILD.md](BUILD.md))
- macOS with Automator (included by default)

### Creating Quick Actions

#### 1. "Flatten PDF" Quick Action

This creates a rasterized PDF that looks identical to the original but with all text and vector elements flattened to images.

**Steps:**
1. Open **Automator** (Applications > Automator)
2. Choose **Quick Action** (not Workflow)
3. Configure at the top:
   - **Workflow receives**: `PDF files`
   - **In**: `Finder`
4. Add **"Run Shell Script"** action from the left panel
5. Configure the shell script:
   - **Pass input**: `as arguments` ⚠️ (Critical setting!)
   - **Shell**: `/bin/bash`

6. **Script content:**

```bash
#!/bin/bash

# Path to your PDF Rasterizer executable (update this path!)
PDF_RASTERIZER="/Users/YOUR_USERNAME/path/to/pdf-redactor/dist/pdf_rasterizer"

for file in "$@"
do
    if [[ "$file" == *.pdf ]]; then
        # Get the directory where the PDF file is located
        pdf_dir=$(dirname "$file")
        
        # Get just the filename without extension for better notification
        filename=$(basename "$file" .pdf)
        
        # Create flattened PDF in same directory as original
        "$PDF_RASTERIZER" "$file" --create-pdf --output-dir "$pdf_dir"
        
        # Show success notification
        if [[ $? -eq 0 ]]; then
            osascript -e "display notification \"${filename}_rasterized.pdf created\" with title \"PDF Flattened Successfully\""
        else
            osascript -e "display notification \"Failed to process $filename\" with title \"PDF Rasterizer Error\""
        fi
    fi
done
```

7. **Save as**: "Flatten PDF"

#### 2. "Convert PDF to Images" Quick Action

This converts PDF pages to individual PNG images.

Follow the same steps but use this script:

```bash
#!/bin/bash

# Path to your PDF Rasterizer executable (update this path!)
PDF_RASTERIZER="/Users/YOUR_USERNAME/path/to/pdf-redactor/dist/pdf_rasterizer"

for file in "$@"
do
    if [[ "$file" == *.pdf ]]; then
        # Get the directory where the PDF file is located
        pdf_dir=$(dirname "$file")
        
        # Get just the filename without extension
        filename=$(basename "$file" .pdf)
        
        # Convert to PNG images at 300 DPI
        "$PDF_RASTERIZER" "$file" --format PNG --dpi 300 --output-dir "$pdf_dir"
        
        # Show success notification
        if [[ $? -eq 0 ]]; then
            osascript -e "display notification \"$filename converted to PNG images\" with title \"PDF to Images Complete\""
        else
            osascript -e "display notification \"Failed to convert $filename\" with title \"PDF Rasterizer Error\""
        fi
    fi
done
```

#### 3. "PDF Options Menu" Quick Action

For more control, create an interactive menu:

```bash
#!/bin/bash

# Path to your PDF Rasterizer executable (update this path!)
PDF_RASTERIZER="/Users/YOUR_USERNAME/path/to/pdf-redactor/dist/pdf_rasterizer"

for file in "$@"
do
    if [[ "$file" == *.pdf ]]; then
        # Get the directory and filename
        pdf_dir=$(dirname "$file")
        filename=$(basename "$file" .pdf)
        
        # Show dialog for options
        action=$(osascript -e 'choose from list {"Flatten PDF", "Convert to PNG (300 DPI)", "Convert to JPEG (600 DPI)", "Get PDF Info"} with prompt "Choose action for PDF:" with title "PDF Rasterizer"')
        
        # Exit if user cancelled
        if [[ "$action" == "false" ]]; then
            exit 0
        fi
        
        case "$action" in
            "Flatten PDF")
                "$PDF_RASTERIZER" "$file" --create-pdf --output-dir "$pdf_dir"
                osascript -e "display notification \"${filename}_rasterized.pdf created\" with title \"PDF Flattened\""
                ;;
            "Convert to PNG (300 DPI)")
                "$PDF_RASTERIZER" "$file" --format PNG --dpi 300 --output-dir "$pdf_dir"
                osascript -e "display notification \"$filename converted to PNG images\" with title \"PNG Conversion Complete\""
                ;;
            "Convert to JPEG (600 DPI)")
                "$PDF_RASTERIZER" "$file" --format JPEG --dpi 600 --output-dir "$pdf_dir"
                osascript -e "display notification \"$filename converted to JPEG images\" with title \"JPEG Conversion Complete\""
                ;;
            "Get PDF Info")
                info=$("$PDF_RASTERIZER" "$file" --info 2>/dev/null)
                osascript -e "display dialog \"$info\" with title \"PDF Information: $filename\" buttons {\"OK\"} default button \"OK\""
                ;;
        esac
    fi
done
```

## Usage

After creating the Quick Actions:

1. **Right-click** any PDF file in Finder
2. Choose **Quick Actions** > **"Flatten PDF"** (or your chosen name)
3. The tool runs automatically
4. A notification appears when complete
5. Output files appear in the same directory as the original

## Important Notes

### ⚠️ Critical Settings
- **Must set "Pass input: as arguments"** in the Run Shell Script action
- **Update the PDF_RASTERIZER path** to match your installation

### 🔧 Path Configuration
Replace this line in all scripts:
```bash
PDF_RASTERIZER="/Users/YOUR_USERNAME/path/to/pdf-redactor/dist/pdf_rasterizer"
```

With your actual path, for example:
```bash
PDF_RASTERIZER="/Users/scattej/Documents/GitHub/personal/pdf-redactor/dist/pdf_rasterizer"
```

### 🛡️ Security Permissions
- macOS may ask for permissions the first time you run a Quick Action
- If the executable is blocked, run: `xattr -d com.apple.quarantine /path/to/pdf_rasterizer`

### 📁 Quick Action Management
- **View/Edit**: System Preferences > Extensions > Finder Extensions
- **Enable/Disable**: Check/uncheck your Quick Actions
- **Delete**: Remove from `/Users/YOUR_USERNAME/Library/Services/`

## Troubleshooting

### Quick Action doesn't appear
- Verify "Workflow receives: PDF files" is set correctly
- Check System Preferences > Extensions > Finder Extensions
- Make sure it's saved as "Quick Action" not "Workflow"

### Nothing happens when clicked
- Check "Pass input: as arguments" is selected
- Verify the PDF_RASTERIZER path is correct
- Test the executable path in Terminal first

### Permission errors
```bash
# Remove quarantine attribute if needed
xattr -d com.apple.quarantine /path/to/pdf_rasterizer

# Check executable permissions
ls -la /path/to/pdf_rasterizer
```

### Debug issues
Add this to the beginning of any script for debugging:
```bash
echo "Debug: $@" > ~/Desktop/debug.log
echo "PWD: $(pwd)" >> ~/Desktop/debug.log
```

## Output Files

- **Flattened PDFs**: `originalname_rasterized.pdf`
- **Images**: `originalname_page_01.png`, `originalname_page_02.png`, etc.
- **Location**: Same directory as the original PDF file

## Multiple File Support

All Quick Actions support processing multiple selected PDF files simultaneously. Simply select multiple PDFs in Finder and run the Quick Action - each file will be processed individually. 