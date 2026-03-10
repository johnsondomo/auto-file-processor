#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Web Scraper - Easy data extraction from websites
Author: johnsondomo
GitHub: https://github.com/johnsondomo/web-scraper

Features:
- Extract data from HTML pages
- Export to CSV/JSON
- Support for CSS selectors
- No dependencies beyond requests/beautifulsoup4

Usage:
    python web_scraper.py --url "https://example.com" --selector "h1"
"""

import argparse
import json
import csv
import sys
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"])
    import requests
    from bs4 import BeautifulSoup


class WebScraper:
    """Simple web scraper for data extraction"""
    
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.response = None
    
    def fetch(self, headers=None):
        """Fetch the webpage"""
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        
        try:
            self.response = requests.get(self.url, headers=headers, timeout=30)
            self.response.raise_for_status()
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            return True
        except Exception as e:
            print(f"Error fetching page: {e}")
            return False
    
    def extract(self, selector, attribute=None):
        """
        Extract data using CSS selector
        
        Args:
            selector: CSS selector (e.g., "h1", ".class", "#id")
            attribute: Optional attribute to extract (e.g., "href", "src")
        
        Returns:
            List of extracted text/attributes
        """
        if not self.soup:
            print("Page not fetched. Call fetch() first.")
            return []
        
        elements = self.soup.select(selector)
        results = []
        
        for elem in elements:
            if attribute:
                value = elem.get(attribute, '')
            else:
                value = elem.get_text(strip=True)
            
            if value:
                results.append(value)
        
        return results
    
    def extract_all(self, rules):
        """
        Extract multiple data points at once
        
        Args:
            rules: Dict of {name: {selector, attribute}}
        
        Returns:
            Dict of extracted data
        """
        results = {}
        
        for name, rule in rules.items():
            selector = rule.get('selector', '')
            attribute = rule.get('attribute', None)
            results[name] = self.extract(selector, attribute)
        
        return results
    
    def to_csv(self, data, filename='output.csv'):
        """Export data to CSV"""
        if not data:
            print("No data to export")
            return
        
        # Flatten if all lists are same length
        keys = list(data.keys())
        if keys:
            lengths = [len(data[k]) for k in keys]
            if len(set(lengths)) == 1:
                # All same length - create rows
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(keys)
                    for i in range(lengths[0]):
                        row = [data[k][i] for k in keys]
                        writer.writerow(row)
                print(f"Exported to {filename}")
            else:
                # Different lengths - export as separate sections
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    for key in keys:
                        writer.writerow([key])
                        for item in data[key]:
                            writer.writerow([item])
                        writer.writerow([])
                print(f"Exported to {filename}")
    
    def to_json(self, data, filename='output.json'):
        """Export data to JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Exported to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Simple Web Scraper - Extract data from websites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Extract all headings
  python web_scraper.py --url "https://example.com" --selector "h1"
  
  # Extract links
  python web_scraper.py --url "https://example.com" --selector "a" --attribute href
  
  # Extract with custom rules (JSON file)
  python web_scraper.py --url "https://example.com" --rules rules.json
  
  # Export to CSV
  python web_scraper.py --url "https://example.com" --selector ".product-title" --output data.csv
        '''
    )
    
    parser.add_argument('--url', '-u', required=True, help='Target URL')
    parser.add_argument('--selector', '-s', help='CSS selector')
    parser.add_argument('--attribute', '-a', help='Attribute to extract (href, src, etc.)')
    parser.add_argument('--rules', '-r', help='JSON file with extraction rules')
    parser.add_argument('--output', '-o', help='Output file (CSV or JSON)')
    parser.add_argument('--format', '-f', choices=['csv', 'json'], default='csv', help='Output format')
    
    args = parser.parse_args()
    
    # Validate URL
    parsed = urlparse(args.url)
    if not parsed.scheme:
        args.url = 'https://' + args.url
        print(f"Using URL: {args.url}")
    
    scraper = WebScraper(args.url)
    
    if not scraper.fetch():
        sys.exit(1)
    
    print(f"✓ Page fetched successfully")
    print(f"  Title: {scraper.soup.title.string if scraper.soup.title else 'N/A'}")
    
    data = {}
    
    if args.rules:
        # Load rules from JSON file
        with open(args.rules, 'r') as f:
            rules = json.load(f)
        data = scraper.extract_all(rules)
    elif args.selector:
        # Single selector
        data['extracted'] = scraper.extract(args.selector, args.attribute)
    else:
        # No selector - show available headings as example
        print("\nNo selector specified. Available headings:")
        for tag in ['h1', 'h2', 'h3']:
            items = scraper.extract(tag)
            if items:
                print(f"\n{tag.upper()} ({len(items)} items):")
                for item in items[:5]:
                    print(f"  - {item[:60]}...")
        sys.exit(0)
    
    # Show results
    print(f"\n✓ Extracted {sum(len(v) for v in data.values())} items")
    
    for key, values in data.items():
        print(f"\n{key} ({len(values)} items):")
        for v in values[:5]:
            print(f"  - {str(v)[:60]}...")
    
    # Export
    if args.output:
        if args.format == 'csv' or args.output.endswith('.csv'):
            scraper.to_csv(data, args.output)
        else:
            scraper.to_json(data, args.output)
    else:
        # Auto-export
        scraper.to_json(data, 'output.json')


if __name__ == '__main__':
    main()
