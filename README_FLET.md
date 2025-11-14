# 🍽️ Chili POS - Food Delivery System (Flet Version)

Modern Point of Sale system built with **Flet** (Python UI framework) inspired by Chili Pos design.

## 🎨 Design Features

This application implements the **Chili Pos UI/UX design** with:

### ✅ Product Grid
- **Responsive 3-column grid layout** with auto-adjusting cards
- **Product cards** with:
  - Large emoji icons with green circular backgrounds
  - Product name and category badges
  - 5-star ratings display
  - Prominent pricing in green
  - Green "Add to Cart" buttons

### ✅ Category Navigation
- **Horizontal scrollable tabs** with emoji icons
- Category count display (e.g., "ทั้งหมด (250)")
- Categories: Breakfast 🍳, Soups 🍲, Pasta 🍝, Burgers 🍔, Drinks ☕, etc.
- Green highlight for active category

### ✅ Search Functionality
- **Icon-enhanced search bar** with 🔍 icon
- Real-time product search
- Enter key support for quick search

### ✅ Shopping Cart Sidebar
- **Table number display** (Table 4)
- Cart items with emoji icons
- **Pricing breakdown**:
  - Subtotal
  - Tax (7%)
  - Total amount (prominent)
- Item quantity tracking
- Remove item functionality

### ✅ Payment Method Selector
- **Three payment options**:
  - 💵 Cash (เงินสด)
  - 💳 Credit/Debit Card (บัตร)
  - 📱 QR Code
- Visual radio button selection
- Expanded height for easy clicking

### ✅ Modern UI Elements
- **Green color scheme** (food/fresh/healthy theme)
- **Dark sidebar navigation** with menu items
- **Material Design 3** components
- Smooth animations and transitions
- Responsive layout

## 🚀 Installation

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

Requirements:
- `flet>=0.24.0` - Modern UI framework
- `ttkbootstrap` - For legacy version
- `pillow` - Image processing

### 2. Setup Database

The application uses SQLite database. Make sure you have the database initialized:

```bash
python database/seed_db.py
```

## 📱 Running the Application

### Desktop Application (Recommended)

```bash
python pos_flet.py
```

This opens the POS system in a **native desktop window**.

### Web Browser Version

Edit `pos_flet.py` line 669:

```python
ft.app(target=main, view=ft.WEB_BROWSER)
```

Then run:

```bash
python pos_flet.py
```

This opens the POS system in your **default web browser**.

### Mobile App

Flet supports iOS and Android. Follow [Flet mobile deployment guide](https://flet.dev/docs/guides/python/packaging-desktop-app/).

## 🏗️ Architecture

### File Structure

```
pos/
├── pos_flet.py           # Main Flet application
├── src/
│   ├── pos_app.py        # Legacy ttkbootstrap version
│   └── views/
│       └── pos_view.py   # ttkbootstrap POS view
├── database/
│   ├── db_manager.py     # Database operations
│   ├── seed_db.py        # Sample data
│   └── __init__.py
├── requirements.txt      # Dependencies
└── README_FLET.md       # This file
```

### Main Components

#### `POSFletApp` Class
Main application class with:
- `build_sidebar()` - Left navigation menu
- `build_header()` - Top header with title
- `build_main_content()` - Products + Cart layout
- `build_search_bar()` - Search functionality
- `build_category_tabs()` - Category filters
- `build_products_grid()` - Product cards grid
- `build_cart_sidebar()` - Shopping cart
- `build_payment_selector()` - Payment methods

#### Database Integration
- Uses `DatabaseManager` from `database/db_manager.py`
- SQLite database for products, categories, and receipts
- CRUD operations for all entities

## 🎯 Key Features

### 1. Product Management
- Load products from database
- Display with emoji icons based on category
- Filter by category
- Search by product name
- Responsive grid layout (3 columns)

### 2. Shopping Cart
- Add items to cart
- Automatic quantity increment for duplicates
- Visual cart items with emoji icons
- Real-time total calculation
- Subtotal, tax (7%), and total display
- Remove items functionality

### 3. Checkout Process
- Select payment method (Cash/Card/QR)
- Save receipt to database
- Show success notification
- Clear cart after checkout
- Generate receipt ID

### 4. Category Filtering
- "All" category shows all products
- Individual category filters (Beverages, Food, Desserts, etc.)
- Visual feedback for active category (green highlight)
- Emoji icons for each category

## 🎨 Color Scheme

Following **Chili Pos design**:

- **Primary Green**: `ft.colors.GREEN_700` - Buttons, highlights
- **Light Green**: `ft.colors.GREEN_50` - Product icon backgrounds
- **Dark Sidebar**: `ft.colors.GREY_900` - Navigation sidebar
- **White/Light**: `ft.colors.WHITE`, `ft.colors.GREY_50` - Backgrounds
- **Accent Colors**: Blue, Orange, Purple for different menu items

## 🔧 Customization

### Change Theme

Edit in `POSFletApp.__init__()`:

```python
self.page.theme = ft.Theme(
    color_scheme_seed=ft.colors.GREEN,  # Change to ft.colors.BLUE, etc.
    use_material3=True
)
```

### Add New Categories

1. Add to database via `db_manager.py`
2. Update emoji mapping in `build_category_tabs()`:

```python
category_emojis = {
    'Your Category': '🆕',  # Add your category
    # ... existing categories
}
```

### Modify Tax Rate

Edit in `update_cart_display()`:

```python
self.tax = self.subtotal * 0.07  # Change 0.07 to your tax rate
```

### Change Grid Columns

Edit in `build_products_grid()`:

```python
self.product_grid = ft.GridView(
    runs_count=3,  # Change to 2, 4, 5, etc.
    max_extent=250,
    # ...
)
```

## 📊 Comparison: Flet vs ttkbootstrap

| Feature | Flet | ttkbootstrap |
|---------|------|--------------|
| **Platform** | Windows, Mac, Linux, Web, Mobile | Windows, Mac, Linux |
| **UI Framework** | Flutter (via Flet) | Tkinter |
| **Design** | Material Design 3 | Bootstrap-like themes |
| **Deployment** | Desktop, Web, Mobile | Desktop only |
| **Learning Curve** | Moderate | Easy |
| **Performance** | Excellent | Good |
| **Modern Look** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Responsiveness** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🐛 Troubleshooting

### "Module not found: flet"
```bash
pip install flet
```

### Database Error
```bash
# Reinitialize database
python database/seed_db.py
```

### Application won't start
- Make sure Python 3.8+ is installed
- Check all dependencies are installed
- Try running with `python -m flet pos_flet.py`

### Web browser doesn't open
Change view mode in code:
```python
ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
```

## 📚 Resources

- **Flet Documentation**: https://flet.dev/docs/
- **Flet Examples**: https://github.com/flet-dev/examples
- **Chili Pos Design**: Original UI inspiration
- **Material Design 3**: https://m3.material.io/

## 🎓 Learning Path

1. **Start with Flet basics**: Learn containers, rows, columns
2. **Understand GridView**: For responsive product grid
3. **Master state management**: Using `page.update()`
4. **Explore controls**: Buttons, cards, radio groups
5. **Deploy**: Package for desktop/web/mobile

## 🚀 Future Enhancements

- [ ] Admin dashboard for product management
- [ ] Real-time order tracking
- [ ] Multiple table management
- [ ] Receipt printing to thermal printer
- [ ] Sales analytics and reports
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Customer display screen
- [ ] Kitchen display system (KDS)
- [ ] Integration with payment gateways

## 💡 Tips

1. **Fast development**: Use hot reload with `flet run --web pos_flet.py`
2. **Debugging**: Add `print()` statements to track state changes
3. **Testing**: Use Flet's built-in testing framework
4. **Deployment**: Use `flet build` for production builds

## 📄 License

This project is for educational purposes. Chili Pos design is used as inspiration.

## 👨‍💻 Development

Built with ❤️ using:
- **Flet** - Modern Python UI framework
- **SQLite** - Lightweight database
- **Material Design 3** - UI design system

---

**Happy Coding! 🎉**

For the ttkbootstrap version, see [README.md](README.md)
