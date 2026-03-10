#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Social Media Downloader - Download images/videos from social media
Author: johnsondomo
GitHub: https://github.com/johnsondomo/auto-file-processor

⚠️ For personal use only. Respect copyright and terms of service.

Usage:
    python social_downloader.py --url "https://..." --output ./downloads
"""

import argparse
import os
import sys
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"])
    import requests
    from bs4 import BeautifulSoup


class SocialDownloader:
    """Download media from social platforms"""
    
    def __init__(self, output_dir='./downloads'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.downloaded = 0
    
    def detect_platform(self, url):
        """Detect social media platform from URL"""
        if 'instagram.com' in url:
            return 'instagram'
        elif 'twitter.com' in url or 'x.com' in url:
            return 'twitter'
        elif 'pinterest.com' in url:
            return 'pinterest'
        elif 'tiktok.com' in url:
            return 'tiktok'
        else:
            return 'unknown'
    
    def download_file(self, url, filename):
        """Download a single file"""
        try:
            response = requests.get(url, headers=self.headers, stream=True, timeout=30)
            response.raise_for_status()
            
            filepath = self.output_dir / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ Downloaded: {filename}")
            self.downloaded += 1
            return True
        except Exception as e:
            print(f"✗ Failed: {filename} - {e}")
            return False
    
    def download_instagram(self, url):
        """
        Download Instagram media
        Note: This is a simplified version. For full functionality, use Instagram API.
        """
        print(f"Processing Instagram URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all images
            images = soup.find_all('img', src=True)
            
            for i, img in enumerate(images):
                src = img['src']
                if 'instagram.com' in src or src.startswith('http'):
                    ext = '.jpg'
                    filename = f"instagram_{i+1:03d}{ext}"
                    self.download_file(src, filename)
            
            print(f"\nDownloaded {self.downloaded} items")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def download_pinterest(self, url):
        """Download Pinterest images"""
        print(f"Processing Pinterest URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            images = soup.find_all('img', src=True)
            
            for i, img in enumerate(images):
                src = img.get('src') or img.get('data-src')
                if src and src.startswith('http'):
                    ext = os.path.splitext(urlparse(src).path)[1] or '.jpg'
                    filename = f"pinterest_{i+1:03d}{ext}"
                    self.download_file(src, filename)
            
            print(f"\nDownloaded {self.downloaded} items")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def download_generic(self, url):
        """Download from generic URL (direct image/video link)"""
        print(f"Processing URL: {url}")
        
        try:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            if not filename or '.' not in filename:
                filename = f"download_{self.downloaded+1}.jpg"
            
            self.download_file(url, filename)
            
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Social Media Downloader - Download images/videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Download from URL
  python social_downloader.py --url "https://..."
  
  # Specify output directory
  python social_downloader.py --url "https://..." --output ./my-downloads
  
  # Multiple URLs
  python social_downloader.py --url "url1" --url "url2" --url "url3"

Supported Platforms:
  - Instagram (images)
  - Pinterest (images)
  - Twitter/X (limited)
  - Generic direct links

⚠️ Disclaimer: For personal use only. Respect copyright!
        '''
    )
    
    parser.add_argument('--url', '-u', action='append', required=True, help='URL(s) to download from')
    parser.add_argument('--output', '-o', default='./downloads', help='Output directory')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Social Media Downloader")
    print("=" * 50)
    print(f"Output: {os.path.abspath(args.output)}\n")
    
    downloader = SocialDownloader(args.output)
    
    for url in args.url:
        platform = downloader.detect_platform(url)
        print(f"\nPlatform: {platform}")
        print("-" * 40)
        
        if platform == 'instagram':
            downloader.download_instagram(url)
        elif platform == 'pinterest':
            downloader.download_pinterest(url)
        else:
            downloader.download_generic(url)
    
    print("\n" + "=" * 50)
    print(f"Total downloaded: {downloader.downloaded} files")
    print(f"Saved to: {os.path.abspath(args.output)}")
    print("=" * 50)


if __name__ == '__main__':
    main()
