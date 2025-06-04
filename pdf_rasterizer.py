#!/usr/bin/env python3
"""
PDF Rasterizer - Convert PDF pages to rasterized images

This script converts each page of a PDF document into high-quality raster images,
ensuring that all text and vector elements are flattened into bitmap format.
"""

import os
import sys
import argparse
import io
from pathlib import Path
from typing import List, Tuple, Optional
import fitz  # PyMuPDF
from PIL import Image, ImageEnhance
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PDFRasterizer:
    """
    A class to handle PDF rasterization with various options and quality settings.
    """
    
    def __init__(self, dpi: int = 300, output_format: str = 'PNG'):
        """
        Initialize the PDF rasterizer.
        
        Args:
            dpi (int): Resolution for rasterization (default: 300)
            output_format (str): Output image format ('PNG', 'JPEG', 'TIFF')
        """
        self.dpi = dpi
        self.output_format = output_format.upper()
        self.zoom_factor = dpi / 72.0  # PDF default is 72 DPI
        
        # Validate output format
        if self.output_format not in ['PNG', 'JPEG', 'JPG', 'TIFF', 'BMP']:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def rasterize_pdf(self, input_path: str, output_dir: str = None, 
                     filename_prefix: str = None, enhance_quality: bool = True) -> List[str]:
        """
        Rasterize all pages of a PDF document.
        
        Args:
            input_path (str): Path to the input PDF file
            output_dir (str): Directory to save output images (default: same as input)
            filename_prefix (str): Prefix for output filenames (default: input filename)
            enhance_quality (bool): Apply image enhancement for better quality
            
        Returns:
            List[str]: List of paths to the generated image files
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input PDF file not found: {input_path}")
        
        # Set up output directory and filename prefix
        if output_dir is None:
            output_dir = input_path.parent
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        if filename_prefix is None:
            filename_prefix = input_path.stem
        
        logger.info(f"Starting rasterization of {input_path}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Resolution: {self.dpi} DPI")
        logger.info(f"Output format: {self.output_format}")
        
        # Open the PDF document
        try:
            pdf_document = fitz.open(str(input_path))
        except Exception as e:
            raise RuntimeError(f"Failed to open PDF: {e}")
        
        output_files = []
        total_pages = len(pdf_document)
        
        logger.info(f"Processing {total_pages} pages...")
        
        for page_num in range(total_pages):
            try:
                # Get the page
                page = pdf_document[page_num]
                
                # Create transformation matrix for desired DPI
                mat = fitz.Matrix(self.zoom_factor, self.zoom_factor)
                
                # Render page to pixmap
                pix = page.get_pixmap(matrix=mat, alpha=False)
                
                # Convert to PIL Image
                img_data = pix.tobytes("ppm")
                pil_image = Image.open(io.BytesIO(img_data))
                
                # Apply quality enhancements if requested
                if enhance_quality:
                    pil_image = self._enhance_image(pil_image)
                
                # Generate output filename
                page_number = str(page_num + 1).zfill(len(str(total_pages)))
                filename = f"{filename_prefix}_page_{page_number}.{self.output_format.lower()}"
                output_path = output_dir / filename
                
                # Save the image
                save_kwargs = self._get_save_kwargs()
                pil_image.save(str(output_path), **save_kwargs)
                output_files.append(str(output_path))
                
                logger.info(f"Processed page {page_num + 1}/{total_pages}: {filename}")
                
            except Exception as e:
                logger.error(f"Failed to process page {page_num + 1}: {e}")
                continue
        
        pdf_document.close()
        logger.info(f"Rasterization complete. Generated {len(output_files)} images.")
        
        return output_files
    
    def create_pdf_from_images(self, image_paths: List[str], output_pdf_path: str) -> str:
        """
        Create a PDF file from a list of image files.
        
        Args:
            image_paths (List[str]): List of paths to image files
            output_pdf_path (str): Path for the output PDF file
            
        Returns:
            str: Path to the created PDF file
        """
        if not image_paths:
            raise ValueError("No image paths provided")
        
        logger.info(f"Creating PDF from {len(image_paths)} images...")
        logger.info(f"Output PDF: {output_pdf_path}")
        
        try:
            # Open all images
            images = []
            for i, img_path in enumerate(image_paths):
                if not Path(img_path).exists():
                    logger.warning(f"Image file not found: {img_path}")
                    continue
                
                img = Image.open(img_path)
                # Convert to RGB if necessary (for PDF compatibility)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
                logger.info(f"Loaded image {i + 1}/{len(image_paths)}: {Path(img_path).name}")
            
            if not images:
                raise RuntimeError("No valid images found to create PDF")
            
            # Save as PDF
            # The first image is used as the base, and the rest are appended
            images[0].save(
                output_pdf_path,
                format='PDF',
                save_all=True,
                append_images=images[1:] if len(images) > 1 else [],
                resolution=self.dpi
            )
            
            logger.info(f"Successfully created PDF with {len(images)} pages")
            return output_pdf_path
            
        except Exception as e:
            raise RuntimeError(f"Failed to create PDF: {e}")
    
    def rasterize_and_recreate_pdf(self, input_path: str, output_dir: str = None, 
                                   filename_prefix: str = None, enhance_quality: bool = True,
                                   keep_images: bool = False) -> Tuple[str, List[str]]:
        """
        Rasterize a PDF and recreate it as a new PDF with flattened images.
        
        Args:
            input_path (str): Path to the input PDF file
            output_dir (str): Directory to save output files (default: same as input)
            filename_prefix (str): Prefix for output filenames (default: input filename)
            enhance_quality (bool): Apply image enhancement for better quality
            keep_images (bool): Whether to keep the individual image files
            
        Returns:
            Tuple[str, List[str]]: Path to the new PDF and list of image files created
        """
        # First, rasterize the PDF to images
        image_files = self.rasterize_pdf(
            input_path=input_path,
            output_dir=output_dir,
            filename_prefix=filename_prefix,
            enhance_quality=enhance_quality
        )
        
        # Determine output PDF path
        input_path = Path(input_path)
        if output_dir is None:
            output_dir = input_path.parent
        else:
            output_dir = Path(output_dir)
        
        if filename_prefix is None:
            filename_prefix = input_path.stem
        
        output_pdf_path = output_dir / f"{filename_prefix}_rasterized.pdf"
        
        # Create PDF from images
        created_pdf = self.create_pdf_from_images(image_files, str(output_pdf_path))
        
        # Optionally remove individual image files
        if not keep_images:
            logger.info("Cleaning up individual image files...")
            for img_file in image_files:
                try:
                    Path(img_file).unlink()
                    logger.info(f"Deleted: {Path(img_file).name}")
                except Exception as e:
                    logger.warning(f"Failed to delete {img_file}: {e}")
        
        return created_pdf, image_files
    
    def _enhance_image(self, image: Image.Image) -> Image.Image:
        """
        Apply image enhancements for better quality.
        
        Args:
            image (Image.Image): Input PIL image
            
        Returns:
            Image.Image: Enhanced PIL image
        """
        # Enhance contrast slightly
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
        
        # Enhance sharpness slightly
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
        
        return image
    
    def _get_save_kwargs(self) -> dict:
        """
        Get appropriate save parameters for the output format.
        
        Returns:
            dict: Save parameters for PIL Image.save()
        """
        if self.output_format in ['JPEG', 'JPG']:
            return {
                'quality': 95,
                'optimize': True,
                'progressive': True
            }
        elif self.output_format == 'PNG':
            return {
                'optimize': True,
                'compress_level': 6
            }
        elif self.output_format == 'TIFF':
            return {
                'compression': 'lzw',
                'tiffinfo': {317: 2}  # Predictor for better compression
            }
        else:
            return {}
    
    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        Get information about a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            dict: PDF information including page count, dimensions, etc.
        """
        try:
            pdf_document = fitz.open(pdf_path)
            info = {
                'page_count': len(pdf_document),
                'title': pdf_document.metadata.get('title', 'Unknown'),
                'author': pdf_document.metadata.get('author', 'Unknown'),
                'subject': pdf_document.metadata.get('subject', 'None'),
                'pages_info': []
            }
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                rect = page.rect
                info['pages_info'].append({
                    'page': page_num + 1,
                    'width': rect.width,
                    'height': rect.height,
                    'rotation': page.rotation
                })
            
            pdf_document.close()
            return info
            
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF info: {e}")


def main():
    """
    Main function to handle command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Rasterize PDF pages to high-quality images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.pdf
  %(prog)s document.pdf --dpi 600 --format JPEG
  %(prog)s document.pdf --output-dir ./images --prefix "doc"
  %(prog)s document.pdf --info
  %(prog)s document.pdf --create-pdf
  %(prog)s document.pdf --create-pdf --keep-images
        """
    )
    
    parser.add_argument('input_pdf', help='Path to the input PDF file')
    parser.add_argument('--dpi', type=int, default=300,
                       help='Resolution in DPI (default: 300)')
    parser.add_argument('--format', default='PNG',
                       choices=['PNG', 'JPEG', 'JPG', 'TIFF', 'BMP'],
                       help='Output image format (default: PNG)')
    parser.add_argument('--output-dir', help='Output directory (default: same as input)')
    parser.add_argument('--prefix', help='Filename prefix (default: input filename)')
    parser.add_argument('--no-enhance', action='store_true',
                       help='Disable image quality enhancement')
    parser.add_argument('--info', action='store_true',
                       help='Show PDF information and exit')
    parser.add_argument('--create-pdf', action='store_true',
                       help='Create a new PDF from rasterized images (flattened PDF)')
    parser.add_argument('--keep-images', action='store_true',
                       help='Keep individual image files when creating PDF (only with --create-pdf)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize rasterizer
        rasterizer = PDFRasterizer(dpi=args.dpi, output_format=args.format)
        
        # Show PDF info if requested
        if args.info:
            info = rasterizer.get_pdf_info(args.input_pdf)
            print(f"\nPDF Information:")
            print(f"Title: {info['title']}")
            print(f"Author: {info['author']}")
            print(f"Subject: {info['subject']}")
            print(f"Pages: {info['page_count']}")
            print(f"\nPage Details:")
            for page_info in info['pages_info']:
                print(f"  Page {page_info['page']}: "
                      f"{page_info['width']:.1f}x{page_info['height']:.1f} pts "
                      f"(rotation: {page_info['rotation']}°)")
            return
        
        # Create flattened PDF if requested
        if args.create_pdf:
            output_pdf, image_files = rasterizer.rasterize_and_recreate_pdf(
                input_path=args.input_pdf,
                output_dir=args.output_dir,
                filename_prefix=args.prefix,
                enhance_quality=not args.no_enhance,
                keep_images=args.keep_images
            )
            
            print(f"\nSuccessfully created rasterized PDF:")
            print(f"  {output_pdf}")
            
            if args.keep_images:
                print(f"\nAlso generated {len(image_files)} individual images:")
                for file_path in image_files:
                    print(f"  {file_path}")
            else:
                print(f"\nTemporary images were cleaned up after PDF creation.")
        else:
            # Standard rasterization to images only
            output_files = rasterizer.rasterize_pdf(
                input_path=args.input_pdf,
                output_dir=args.output_dir,
                filename_prefix=args.prefix,
                enhance_quality=not args.no_enhance
            )
            
            print(f"\nSuccessfully generated {len(output_files)} images:")
            for file_path in output_files:
                print(f"  {file_path}")
            
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 