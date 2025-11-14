# Point of Sale (POS) System

A modern Point of Sale application built with Python and ttkbootstrap.

## Features

- 🛒 **Product Management**: Browse and search products
- 🛍️ **Shopping Cart**: Add, remove, and manage cart items
- 💰 **Checkout**: Process sales and generate receipts
- 📊 **Receipt History**: All transactions are saved to JSON
- 🎨 **Modern UI**: Beautiful interface using ttkbootstrap

## Requirements

- Python 3.8 or higher
- ttkbootstrap
- pillow

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python src/pos_app.py
```

## Project Structure

```
pos/
├── src/
│   └── pos_app.py       # Main application file
├── data/
│   ├── products.json    # Product database
│   └── receipts.json    # Sales receipts (generated)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Features Overview

### Product Display
- Products are displayed in a grid layout
- Each product card shows name, price, and category
- Easy-to-use "Add to Cart" button

### Shopping Cart
- Real-time cart updates
- Quantity management (automatically increases for duplicate items)
- Remove items functionality
- Live total calculation

### Checkout
- One-click checkout process
- Receipt generation with timestamp
- All receipts saved to `data/receipts.json`

### Search
- Search products by name
- Real-time filtering

## Customization

### Adding Products
Edit `data/products.json` to add or modify products:
```json
{
  "id": 13,
  "name": "Product Name",
  "price": 99.99,
  "category": "Category Name"
}
```

### Changing Theme
The application uses the "cosmo" theme by default. Available themes:
- cosmo, flatly, litera, minty, lumen, sandstone, yeti, pulse, united, morph, journal
- darkly, superhero, solar, cyborg, vapor, simplex, cerculean

Change the theme in `pos_app.py`:
```python
root = ttk.Window(themename="your-theme-name")
```

## Data Storage

All data is stored in JSON format in the `data/` directory:
- `products.json`: Product catalog
- `receipts.json`: Transaction history (auto-generated)

## License

MIT License
"# pos-python-flet" 
