#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Tools - Merge, Split, Convert PDFs
Author: johnsondomo
GitHub: https://github.com/johnsondomo/auto-file-processor

Usage:
    python pdf_tools.py merge *.pdf -o merged.pdf
    python pdf_tools.py split document.pdf
    python pdf_tools.py images-to-pdf *.jpg -o output.pdf
"""

import argparse
import sys
import os
from pathlib import Path

# Try to import pypdf, install if not available
try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Installing pypdf...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    from pypdf import PdfReader, PdfWriter

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: Pillow not installed. Image-to-PDF disabled.")


class PDFTools:
    """PDF manipulation utilities"""
    
    @staticmethod
    def merge(pdf_files, output='merged.pdf'):
        """Merge multiple PDFs into one"""
        print(f"Merging {len(pdf_files)} PDFs...")
        
        writer = PdfWriter()
        
        for pdf in pdf_files:
            try:
                reader = PdfReader(pdf)
                for page in reader.pages:
                    writer.add_page(page)
                print(f"  ✓ Added: {pdf} ({len(reader.pages)} pages)")
            except Exception as e:
                print(f"  ✗ Failed: {pdf} - {e}")
        
        with open(output, 'wb') as f:
            writer.write(f)
        
        print(f"\n✓ Merged into: {output}")
        return output
    
    @staticmethod
    def split(pdf_file, output_dir='./split'):
        """Split PDF into individual pages"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        print(f"Splitting: {pdf_file}")
        reader = PdfReader(pdf_file)
        
        for i, page in enumerate(reader.pages, 1):
            writer = PdfWriter()
            writer.add_page(page)
            
            output = Path(output_dir) / f"page_{i:03d}.pdf"
            with open(output, 'wb') as f:
                writer.write(f)
            print(f"  ✓ {output.name}")
        
        print(f"\n✓ Split into {len(reader.pages)} files in {output_dir}/")
        return output_dir
    
    @staticmethod
    def images_to_pdf(image_files, output='output.pdf'):
        """Convert images to PDF"""
        if not PIL_AVAILABLE:
            print("Error: Pillow library required. Run: pip install Pillow")
            return None
        
        print(f"Converting {len(image_files)} images to PDF...")
        
        images = []
        for img_path in image_files:
            try:
                img = Image.open(img_path)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                images.append(img)
                print(f"  ✓ Added: {img_path}")
            except Exception as e:
                print(f"  ✗ Failed: {img_path} - {e}")
        
        if images:
            images[0].save(output, save_all=True, append_images=images[1:])
            print(f"\n✓ Created: {output}")
            return output
        else:
            print("No valid images found")
            return None
    
    @staticmethod
    def extract_images(pdf_file, output_dir='./images'):
        """Extract images from PDF"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        print(f"Extracting images from: {pdf_file}")
        reader = PdfReader(pdf_file)
        
        count = 0
        for i, page in enumerate(reader.pages, 1):
            try:
                images = page.images
                for j, img in enumerate(images):
                    try:
                        img_data = img.data
                        ext = img.name.split('.')[-1] if '.' in img.name else 'png'
                        output = Path(output_dir) / f"page{i}_img{j}.{ext}"
                        with open(output, 'wb') as f:
                            f.write(img_data)
                        count += 1
                        print(f"  ✓ {output.name}")
                    except:
                        pass
            except Exception as e:
                print(f"  Page {i}: {e}")
        
        print(f"\n✓ Extracted {count} images to {output_dir}/")
        return output_dir


def main():
    parser = argparse.ArgumentParser(
        description='PDF Tools - Merge, Split, Convert PDFs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Merge PDFs
  python pdf_tools.py merge file1.pdf file2.pdf file3.pdf -o merged.pdf
  
  # Split PDF
  python pdf_tools.py split document.pdf
  
  # Images to PDF
  python pdf_tools.py images-to-pdf *.jpg -o album.pdf
  
  # Extract images from PDF
  python pdf_tools.py extract-images document.pdf
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Merge
    merge_parser = subparsers.add_parser('merge', help='Merge PDFs')
    merge_parser.add_argument('pdfs', nargs='+', help='PDF files to merge')
    merge_parser.add_argument('-o', '--output', default='merged.pdf', help='Output file')
    
    # Split
    split_parser = subparsers.add_parser('split', help='Split PDF')
    split_parser.add_argument('pdf', help='PDF file to split')
    split_parser.add_argument('-o', '--output', default='./split', help='Output directory')
    
    # Images to PDF
    img_parser = subparsers.add_parser('images-to-pdf', help='Convert images to PDF')
    img_parser.add_argument('images', nargs='+', help='Image files')
    img_parser.add_argument('-o', '--output', default='output.pdf', help='Output PDF')
    
    # Extract images
    ext_parser = subparsers.add_parser('extract-images', help='Extract images from PDF')
    ext_parser.add_argument('pdf', help='PDF file')
    ext_parser.add_argument('-o', '--output', default='./images', help='Output directory')
    
    args = parser.parse_args()
    
    if args.command == 'merge':
        PDFTools.merge(args.pdfs, args.output)
    elif args.command == 'split':
        PDFTools.split(args.pdf, args.output)
    elif args.command == 'images-to-pdf':
        PDFTools.images_to_pdf(args.images, args.output)
    elif args.command == 'extract-images':
        PDFTools.extract_images(args.pdf, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
