#!/usr/bin/env python3
"""
Example usage of the PDFRasterizer class

This script demonstrates how to use the PDFRasterizer programmatically
rather than through the command-line interface.
"""

from pdf_rasterizer import PDFRasterizer
import os

def example_basic_usage():
    """Example of basic PDF rasterization"""
    print("=== Basic Usage Example ===")
    
    # Initialize rasterizer with default settings (300 DPI, PNG format)
    rasterizer = PDFRasterizer()
    
    # Example PDF file (you would replace this with your actual PDF)
    pdf_file = "example.pdf"
    
    if os.path.exists(pdf_file):
        try:
            # Get PDF information first
            info = rasterizer.get_pdf_info(pdf_file)
            print(f"PDF Title: {info['title']}")
            print(f"Pages: {info['page_count']}")
            
            # Rasterize the PDF
            output_files = rasterizer.rasterize_pdf(pdf_file)
            
            print(f"Successfully created {len(output_files)} images:")
            for file_path in output_files:
                print(f"  - {file_path}")
                
        except Exception as e:
            print(f"Error processing PDF: {e}")
    else:
        print(f"PDF file '{pdf_file}' not found. Please provide a valid PDF file.")

def example_advanced_usage():
    """Example of advanced PDF rasterization with custom settings"""
    print("\n=== Advanced Usage Example ===")
    
    # Initialize rasterizer with custom settings
    rasterizer = PDFRasterizer(dpi=600, output_format='JPEG')
    
    pdf_file = "example.pdf"
    
    if os.path.exists(pdf_file):
        try:
            # Rasterize with custom options
            output_files = rasterizer.rasterize_pdf(
                input_path=pdf_file,
                output_dir="./high_quality_images",
                filename_prefix="hq_doc",
                enhance_quality=True
            )
            
            print(f"Created {len(output_files)} high-quality JPEG images at 600 DPI")
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
    else:
        print(f"PDF file '{pdf_file}' not found.")

def example_pdf_info():
    """Example of extracting PDF information"""
    print("\n=== PDF Information Example ===")
    
    rasterizer = PDFRasterizer()
    pdf_file = "example.pdf"
    
    if os.path.exists(pdf_file):
        try:
            info = rasterizer.get_pdf_info(pdf_file)
            
            print(f"Title: {info['title']}")
            print(f"Author: {info['author']}")
            print(f"Subject: {info['subject']}")
            print(f"Total Pages: {info['page_count']}")
            print("\nPage Details:")
            
            for page_info in info['pages_info']:
                print(f"  Page {page_info['page']}: "
                      f"{page_info['width']:.1f} x {page_info['height']:.1f} pts "
                      f"(rotation: {page_info['rotation']}°)")
                
        except Exception as e:
            print(f"Error reading PDF info: {e}")
    else:
        print(f"PDF file '{pdf_file}' not found.")

def example_different_formats():
    """Example of creating images in different formats"""
    print("\n=== Multiple Format Example ===")
    
    pdf_file = "example.pdf"
    
    if os.path.exists(pdf_file):
        formats = ['PNG', 'JPEG', 'TIFF']
        
        for fmt in formats:
            print(f"\nCreating {fmt} images...")
            
            try:
                rasterizer = PDFRasterizer(dpi=300, output_format=fmt)
                output_files = rasterizer.rasterize_pdf(
                    input_path=pdf_file,
                    output_dir=f"./{fmt.lower()}_images",
                    filename_prefix=f"doc_{fmt.lower()}"
                )
                print(f"  Created {len(output_files)} {fmt} images")
                
            except Exception as e:
                print(f"  Error creating {fmt} images: {e}")
    else:
        print(f"PDF file '{pdf_file}' not found.")

if __name__ == "__main__":
    print("PDF Rasterizer - Example Usage")
    print("=" * 40)
    
    # Note: Create a sample PDF file named 'example.pdf' to test these examples
    print("Note: These examples expect a file named 'example.pdf' in the current directory.")
    print("Replace 'example.pdf' with the path to your actual PDF file.\n")
    
    # Run examples
    example_basic_usage()
    example_advanced_usage()
    example_pdf_info()
    example_different_formats()
    
    print("\n" + "=" * 40)
    print("Examples complete!") 