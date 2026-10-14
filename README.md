# Amazon Clone (Flask + HTML/CSS/JS + Neon PostgreSQL)

A full-featured Amazon clone built with a **Flask** backend, authentic **HTML5, CSS3, and JavaScript** frontend, and **Neon PostgreSQL** serverless cloud database.

---

## 🚀 Features & Capabilities

### 1. Amazon Navigation & Header
- **Amazon Logo**: Resets filters and scrolls to top smoothly.
- **Deliver To Selector**: Interactive modal to select city or enter a custom postal code. Updates delivery estimates across the entire storefront in real-time.
- **Search Bar with Real-Time Autocomplete**: Live suggestions dropdown with product thumbnails, prices, and direct navigation.
- **Department Filter**: Dropdown to scope search to any department (Electronics, Computers, Home & Kitchen, Fashion, Books, Beauty).
- **Language Selector**: Preferences modal (EN, ES, DE, FR, HI).
- **Accounts & Lists**: Dropdown with Account shortcuts, Sign In, Register, Switch to Demo Account, and Sign Out.
- **Returns & Orders**: Quick access to past orders and live package tracking.
- **Cart Badge**: Real-time badge counter synchronized with Neon PostgreSQL and session storage.

### 2. Secondary Sub-Nav & Amazon "All" Drawer
- **Hamburger Menu (`☰ All`)**: Slide-out navigation drawer with department links, trending categories, and account settings.
- **Quick Links**: Today's Deals, Best Sellers, Electronics, Computers, Home & Kitchen, Fashion, Books, Gift Cards, Customer Service, and Sell on Amazon.

### 3. Hero Carousel Banner
- Auto-rotating promotional banners with previous/next navigation buttons.
- Bottom gradient fade blending into product cards below.

### 4. Amazon 4-in-1 Quad Cards
- Interactive 4-quadrant cards for Electronics, Home & Kitchen, Fashion, and Quick Services.

### 5. Product Catalog & Faceted Filters
- **Filter Sidebar**:
  - Filter by Department / Category.
  - Filter by Customer Rating (4★ & Up, 4.5★ & Up).
  - Filter by Price (Under \$25, \$25–\$50, \$50–\$100, \$100–\$500, \$500+, or Custom Min/Max range).
  - Special Offers: Prime eligible only, Today's Deals only, Best Sellers only.
- **Sorting**: Featured, Price: Low to High, Price: High to Low, Avg. Customer Review, Newest Arrivals.

### 6. Interactive Product Detail Modal
- Image gallery with clickable thumbnails and image zoom preview.
- Amazon's Choice & #1 Best Seller badges.
- Pricing with discount percentages, typical price, and Prime delivery promise.
- Stock availability and Quantity selector (1–10).
- **Add to Cart**, **Buy Now** (instant direct checkout), and **Add to Wish List**.
- "About this item" bulleted features and technical specifications.
- **Verified Customer Reviews**:
  - Star ratings breakdown.
  - Interactive **Write a Review** form: submit ratings (1–5 stars), review headline, and detailed feedback that writes directly to Neon PostgreSQL and recalculates average rating.

### 7. Slide-Over Shopping Cart
- Slide-over drawer with active cart items and "Saved for Later" section.
- Quantity adjuster (`[-] [qty] [+]`), item removal, and "Save for later" toggle.
- Free delivery qualification progress bar.
- Subtotal calculation in real-time.

### 8. Multi-Step Checkout System
- **Step 1: Shipping Address**: Pre-filled with active user profile, or editable.
- **Step 2: Payment Method**: Amazon Pay Balance, Credit/Debit Card (Visa ending in 4242), or Cash on Delivery (COD).
- **Step 3: Delivery Options**: FREE Two-Day Shipping or Priority One-Day Shipping (+\$4.99).
- **Atomic Database Transaction**: Verifies inventory, decrements stock in `retail_inventory.fact_fba_inventory_daily`, creates order in `retail_sales.fact_orders`, records line items in `retail_sales.fact_order_items`, and clears cart.
- **Order Confirmation Receipt**: Displays unique Order ID, Tracking number, Estimated delivery date, and total.

### 9. Your Orders & Package Tracking
- Visual multi-step package tracker:
  `[Ordered] ──► [Shipped] ──► [Out for Delivery] ──► [Delivered]`
- Action buttons: "Buy it again", "View Invoice", and "Cancel Order" (restores stock back to inventory).

### 10. Wishlist (Shopping List)
- 1-click heart toggle on product cards and detail modal.
- Wishlist modal with "Move to Cart" and "Remove".

### 11. User Authentication & Profile
- Sign In & Create Account modal.
- 1-Click **Switch to Demo Account (Alex Mercer)** for instant testing without typing credentials.
- Password hashing with Werkzeug security.

### 12. Customer Service & Support Hub
- Quick help cards (Orders, Returns & Refunds, Shipping Rates).
- Interactive simulated AI support assistant for immediate queries.

---

## 🛠️ Tech Stack & Database Architecture

- **Backend**: Python 3.10+ / Flask
- **Database**: Neon Serverless PostgreSQL (`sa-east-1` AWS pooler)
- **Frontend**: HTML5, Modern CSS3 (Amazon Ember styling, responsive design), Vanilla JavaScript (ES6+ fetch API)
- **Icons**: FontAwesome 6 (CDN)

### Neon Database Schemas:
- `catalog.dim_categories`
- `catalog.dim_products`
- `catalog.dim_reviews`
- `customers.dim_customers`
- `customers.cart_items`
- `customers.wishlists`
- `retail_inventory.fact_fba_inventory_daily`
- `retail_sales.fact_orders`
- `retail_sales.fact_order_items`
- `retail_traffic.fact_glance_views`
- `fulfillment.dim_fulfillment_centers`

---

## 🏃 Getting Started

### 1. Environment Configuration
Set your Neon connection URL and a unique Flask session key in `.env`:
```ini
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
FLASK_SECRET_KEY=replace-with-a-random-secret
FLASK_DEBUG=false
```
Generate a random session key with `python -c "import secrets; print(secrets.token_hex(32))"`.

### 2. Run the Store
Start the Flask server:
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Run Automated Tests
Execute the comprehensive 13-point test suite:
```bash
python test_suite.py
```

## Deploy to Vercel

1. Import `poruri-santhosh/AMAZON-CLONE` from the Vercel dashboard. Vercel detects the Flask app in `app.py`.
2. Add `DATABASE_URL` and `FLASK_SECRET_KEY` under the project's Environment Variables. Generate a unique value for `FLASK_SECRET_KEY`; do not reuse the local development value.
3. Make sure the Neon database has been initialized with `schema.sql` and populated as needed.
4. Deploy the project. Vercel requires `FLASK_SECRET_KEY` at startup and will report an error if it is missing.
