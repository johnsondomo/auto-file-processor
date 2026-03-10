# Auto File Processor 📁

A simple yet powerful batch file processing tool that automates repetitive file operations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

---

## ✨ Features

- 🔄 **Batch Rename** - Rename multiple files with custom patterns
- 📝 **Change Extensions** - Bulk modify file extensions
- 📊 **Export File Info** - Generate JSON reports of file metadata
- 🎯 **Filter by Type** - Process specific file types only
- 🔍 **Dry Run Mode** - Preview changes before applying

---

## 🚀 Quick Start

### Installation

No installation required. Just download and run:

```bash
# Make sure you have Python 3.6+
python3 auto_file_processor.py --help
```

### Usage Examples

```bash
# 1. List all files in a directory
python3 auto_file_processor.py /path/to/dir --list

# 2. List files with specific extension
python3 auto_file_processor.py /path/to/dir --list --ext .txt

# 3. Batch rename (preview mode)
python3 auto_file_processor.py /path/to/dir --rename "{index}_{name}" --dry-run

# 4. Batch rename (apply changes)
python3 auto_file_processor.py /path/to/dir --rename "{index}_{name}"

# 5. Change extension (preview)
python3 auto_file_processor.py /path/to/dir --change-ext .txt .md --dry-run

# 6. Change extension (apply)
python3 auto_file_processor.py /path/to/dir --change-ext .txt .md

# 7. Export file information
python3 auto_file_processor.py /path/to/dir --export
```

---

## 📋 Rename Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{name}` | Original filename | `report` |
| `{index}` | Sequential number (3 digits) | `001`, `002` |
| `{date}` | Current date | `20260310` |
| `{prefix}` | Custom prefix | `file` |
| `{suffix}` | Custom suffix | `` |

### Template Examples

```bash
# Add sequential prefix
--rename "{index}_{name}"
# Result: 001_report.txt, 002_summary.txt

# Add date prefix
--rename "backup_{date}_{name}"
# Result: backup_20260310_report.txt

# Add custom prefix
--rename "processed_{name}"
# Result: processed_report.txt
```

---

## 💡 Use Cases

- 📸 **Photo Organization** - Batch rename photos from events
- 📄 **Document Standardization** -统一 naming conventions
- 🔄 **File Conversion Prep** - Bulk change extensions after conversion
- 📊 **Inventory Reports** - Export file lists for documentation

---

## 🛠️ Custom Development

Need custom features or enterprise deployment?

**Available Services:**
- Custom file processing scripts
- Integration with existing workflows
- GUI version development
- Enterprise batch deployment

**Contact:** [Open an Issue](https://github.com/johnsondomo/auto-file-processor/issues) or email for custom quotes.

**Pricing:** Starting from $30 for custom scripts

---

## ☕ Support This Project

If you find this tool helpful, consider supporting:

- [GitHub Sponsors](https://github.com/sponsors/johnsondomo)
- [Buy Me a Coffee](https://www.buymeacoffee.com/johnsondomo)
- [PayPal](https://paypal.me/johnsondomo)

Your support helps maintain and improve this project! ❤️

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

**Found this useful? Give it a ⭐Star!**
