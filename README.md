# Sonic Lamb Label Generator

A Google Colab notebook for generating PDF labels for Sonic Lamb headphones with barcodes and product information.

## Features
- Generate individual or batch PDF labels
- Support for different SKU variants (H-series and J-series)
- Customer-specific box contents (Customer vs Ample Store)
- Barcode generation for Serial, Model, and SKU
- Automatic PDF merging for batch processing

## Usage
1. Open the notebook in Google Colab
2. Select customer type (Customer or Ample Store)
3. Enter Serial, MAC, and SKU data
4. Generate and download PDF labels

## SKU Types
- **H-series**: Hardcase variants (₹22,999)
- **J-series**: Softcase variants (₹21,999)

## Box Contents
- **Customer**: H-series includes Jute bag
- **Ample Store**: H-series excludes Jute bag
- **J-series**: Always includes Jute bag regardless of customer type
