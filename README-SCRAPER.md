# Simple Web Scraper 🕷️

Easy-to-use web scraping tool for extracting data from websites. No advanced skills required!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

---

## ✨ Features

- 🎯 **CSS Selectors** - Extract data using familiar CSS selectors
- 📊 **Multiple Formats** - Export to CSV or JSON
- 🔗 **Link Extraction** - Get URLs, images, or any attribute
- 📦 **Batch Export** - Extract multiple data points at once
- ⚡ **Auto-Install** - Dependencies installed automatically

---

## 🚀 Quick Start

### Installation

No manual installation needed! Just run:

```bash
python3 web_scraper.py --help
```

Required packages (requests, beautifulsoup4) will be auto-installed.

### Basic Usage

```bash
# Extract all H1 headings
python3 web_scraper.py --url "https://example.com" --selector "h1"

# Extract all links
python3 web_scraper.py --url "https://example.com" --selector "a" --attribute href

# Extract product titles
python3 web_scraper.py --url "https://example.com/products" --selector ".product-title"

# Export to CSV
python3 web_scraper.py --url "https://example.com" --selector "h2" --output results.csv

# Export to JSON
python3 web_scraper.py --url "https://example.com" --selector ".price" --output prices.json
```

---

## 📋 Advanced Usage

### Multiple Data Points (Rules File)

Create a `rules.json` file:

```json
{
  "titles": {
    "selector": "h1",
    "attribute": null
  },
  "links": {
    "selector": "a",
    "attribute": "href"
  },
  "images": {
    "selector": "img",
    "attribute": "src"
  }
}
```

Then run:

```bash
python3 web_scraper.py --url "https://example.com" --rules rules.json --output data.json
```

---

## 💡 Use Cases

### 🛒 E-commerce Price Monitoring
```bash
python3 web_scraper.py --url "https://shop.com/products" \
  --selector ".price" \
  --output prices.csv
```

### 📰 News Article Extraction
```bash
python3 web_scraper.py --url "https://news.com" \
  --selector "article h2" \
  --output headlines.json
```

### 🔗 Link Collector
```bash
python3 web_scraper.py --url "https://directory.com" \
  --selector "a" \
  --attribute href \
  --output links.csv
```

### 📸 Image URL Extractor
```bash
python3 web_scraper.py --url "https://gallery.com" \
  --selector "img" \
  --attribute src \
  --output images.json
```

---

## 🛠️ Custom Development

Need a custom scraper for a specific website?

**Available Services:**
- Custom web scraping scripts
- Scheduled data extraction
- API integration
- Data cleaning & formatting

**Contact:** [Open an Issue](https://github.com/johnsondomo/web-scraper/issues)

**Pricing:** Starting from $50 for custom scrapers

---

## ☕ Support This Project

If you find this tool helpful, consider supporting:

- [GitHub Sponsors](https://github.com/sponsors/johnsondomo)
- [Buy Me a Coffee](https://www.buymeacoffee.com/johnsondomo)
- [PayPal](https://paypal.me/johnsondomo)

Your support helps maintain and improve this project! ❤️

---

## ⚠️ Disclaimer

Please use this tool responsibly:
- Respect website terms of service
- Don't overload servers with rapid requests
- Check robots.txt before scraping
- Use for legitimate purposes only

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

**Found this useful? Give it a ⭐Star!**
