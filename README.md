
# PDF2TXT-OCR: Add OCR Text Layer to PDFs

<img src="https://github.com/user-attachments/assets/b57a03dc-abee-463b-8411-bc078660860c" alt="PDF2TXT-OCR" width="520">

[![Build Status](https://github.com/ocrmypdf/OCRmyPDF/actions/workflows/build.yml/badge.svg)](https://github.com/ocrmypdf/OCRmyPDF/actions/workflows/build.yml) [![PyPI version](https://img.shields.io/pypi/v/ocrmypdf.svg)](https://pypi.org/project/ocrmypdf/) ![Homebrew version](https://img.shields.io/homebrew/v/ocrmypdf.svg) ![ReadTheDocs](https://readthedocs.org/projects/ocrmypdf/badge/?version=latest) ![Supported Python versions](https://img.shields.io/pypi/pyversions/ocrmypdf)

**PDF2TXT-OCR** enhances scanned PDF files by adding an OCR (Optical Character Recognition) text layer, making them searchable and editable.


## Features at a Glance

- Converts PDFs into searchable [PDF/A](https://en.wikipedia.org/wiki/PDF/A) files.
- Accurately places OCR text beneath images for easy copy-pasting.
- Maintains the original image resolution while optimizing file size.
- Deskews and cleans images for improved OCR accuracy (if requested).
- Validates both input and output files for compatibility.
- Distributes tasks across all CPU cores for faster processing.
- Supports [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for over [100 languages](https://github.com/tesseract-ocr/tessdata).
- Handles files with thousands of pages efficiently.
- Built for privacy, ensuring your data remains secure.

![Demo](misc/screencast/demo.svg)

----

## Why Choose PDF2TXT-OCR?

After exploring existing tools, common issues like misplaced OCR text, altered image resolution, oversized output files, and lack of PDF/A support led to the creation of PDF2TXT-OCR. This tool addresses these gaps with precision and reliability.

---

## Installation Guide

PDF2TXT-OCR is compatible with Linux, Windows, macOS, and FreeBSD. Docker images for x64 and ARM are also available.

### Quick Installation

| Platform                    | Command                          |
|-----------------------------|----------------------------------|
| **Debian/Ubuntu**           | `apt install ocrmypdf`          |
| **Fedora**                  | `dnf install ocrmypdf`          |
| **macOS (Homebrew)**        | `brew install ocrmypdf`         |
| **macOS (MacPorts)**        | `port install ocrmypdf`         |
| **FreeBSD**                 | `pkg install py-ocrmypdf`       |
| **Snap Package**            | `snap install ocrmypdf`         |

For other operating systems, refer to the [detailed installation documentation](https://ocrmypdf.readthedocs.io/en/latest/installation.html).

----

## Getting Started

PDF2TXT-OCR is a command-line tool. Here’s a quick example:

```bash
ocrmypdf input_scanned.pdf output_searchable.pdf
```

### Key Options:
- `-l eng+fra` - Specify languages for OCR.
- `--deskew` - Straightens crooked pages.
- `--rotate-pages` - Corrects misaligned pages.
- `--output-type pdfa` - Produces PDF/A files by default.

For a full list of options, use:

```bash
ocrmypdf --help
```

---

## Multilingual OCR

To use OCR for different languages, install Tesseract language packs. For instance:

```bash
# Debian/Ubuntu
apt-get install tesseract-ocr-chi-sim  # Install Chinese (Simplified)

# macOS (Homebrew)
brew install tesseract-lang
```

Specify multiple languages using their ISO 639-3 codes, e.g., `-l eng+fra`.

---

## Advanced Features

- Convert an image into a searchable PDF:
  ```bash
  ocrmypdf input.jpg output.pdf
  ```
- Add OCR to an existing PDF:
  ```bash
  ocrmypdf input.pdf output.pdf
  ```
- Optimize multilingual PDFs:
  ```bash
  ocrmypdf -l eng+spa input.pdf output.pdf
  ```

Check out the [full documentation](https://ocrmypdf.readthedocs.io/en/latest/index.html) for additional examples.

---

## Requirements

- **Python** (compatible versions listed in [PyPI](https://pypi.org/project/ocrmypdf/)).
- **Tesseract OCR** (v4.1.1 or higher).
- **Ghostscript** for PDF processing.

---
## How to Use PDF2TXT-OCR

1. **Install**: Make sure PDF2TXT-OCR is installed on your system.

2. **Basic Command**:
   ```bash
   ocrmypdf input.pdf output.pdf
   ```

3. **Optional Features**:
   - **Straighten pages**: `--deskew`
   - **Fix alignment**: `--rotate-pages`
   - **Set languages**: `-l eng+fra`
   - **PDF/A output**: `--output-type pdfa`

4. **Examples**:
   - Convert image to PDF:  
     ```bash
     ocrmypdf input.jpg output.pdf
     ```
   - Add OCR to multilingual PDF:  
     ```bash
     ocrmypdf -l eng+spa input.pdf output.pdf
     ```

5. **Help**: For all options, run:
   ```bash
   ocrmypdf --help
   ```
---

## Media and Reviews

PDF2TXT-OCR has been featured in leading publications, including:

- **Medium**: [Going Paperless with OCRmyPDF](https://medium.com/@ikirichenko/going-paperless-with-ocrmypdf-e2f36143f46a)
- **Linux Links**: [Excellent Utilities: OCRmyPDF](https://www.linuxlinks.com/excellent-utilities-ocrmypdf-add-ocr-text-layer-scanned-pdfs/)
- **c’t Magazine**: Detailed overview in Germany’s top IT magazine.

---

## Business Inquiries

For feature development, consulting, or integrating PDF2TXT-OCR into larger systems, please get in touch. Support from companies and users helps improve the project.

---

## License

PDF2TXT-OCR is licensed under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/). Other components may use different licenses, as detailed in the source code.

---

## Disclaimer

This software is provided "AS IS" without warranties of any kind, either express or implied.

For further details, visit our [documentation](https://ocrmypdf.readthedocs.io/en/latest/index.html) or report issues on [GitHub](https://github.com/ocrmypdf/OCRmyPDF/issues).

--- 
