-- Amazon Clone Complete Database Schema
-- Compatible with Neon PostgreSQL

CREATE SCHEMA IF NOT EXISTS catalog;
CREATE SCHEMA IF NOT EXISTS customers;
CREATE SCHEMA IF NOT EXISTS fulfillment;
CREATE SCHEMA IF NOT EXISTS retail_traffic;
CREATE SCHEMA IF NOT EXISTS retail_sales;
CREATE SCHEMA IF NOT EXISTS retail_inventory;

-- 1. Dim Categories
CREATE TABLE IF NOT EXISTS catalog.dim_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    icon VARCHAR(50),
    CONSTRAINT uq_dim_categories_name_department UNIQUE (category_name, department)
);

-- 2. Dim Products
CREATE TABLE IF NOT EXISTS catalog.dim_products (
    asin VARCHAR(10) PRIMARY KEY,
    product_title VARCHAR(255) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    category_id INT REFERENCES catalog.dim_categories(category_id),
    standard_price NUMERIC(10, 2) NOT NULL CHECK (standard_price >= 0),
    original_price NUMERIC(10, 2),
    discount_percent INT DEFAULT 0,
    rating NUMERIC(3, 2) DEFAULT 4.5,
    rating_count INT DEFAULT 120,
    image_url VARCHAR(500),
    additional_images JSONB DEFAULT '[]'::jsonb,
    description TEXT,
    features JSONB DEFAULT '[]'::jsonb,
    is_prime_eligible BOOLEAN NOT NULL DEFAULT TRUE,
    is_best_seller BOOLEAN NOT NULL DEFAULT FALSE,
    is_amazons_choice BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Alter table to ensure any missing columns exist on existing databases
ALTER TABLE catalog.dim_products ADD COLUMN IF NOT EXISTS image_url VARCHAR(500);
ALTER TABLE catalog.dim_products ADD COLUMN IF NOT EXISTS additional_images JSONB DEFAULT '[]'::jsonb;
ALTER TABLE catalog.dim_products ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE catalog.dim_products ADD COLUMN IF NOT EXISTS features JSONB DEFAULT '[]'::jsonb;
ALTER TABLE catalog.dim_products ADD COLUMN IF NOT EXISTS rating NUMERIC(3, 2) DEFAULT 4.5;
ALTER TABLE catalog.dim_products ADD COLUMN IF NOT EXISTS rating_count INT DEFAULT 120;
ALTER TABLE catalog.dim_products ADD COLUMN IF NOT EXISTS discount_percent INT DEFAULT 0;
ALTER TABLE catalog.dim_products ADD COLUMN IF NOT EXISTS original_price NUMERIC(10, 2);
ALTER TABLE catalog.dim_products ADD COLUMN IF NOT EXISTS is_best_seller BOOLEAN DEFAULT FALSE;
ALTER TABLE catalog.dim_products ADD COLUMN IF NOT EXISTS is_amazons_choice BOOLEAN DEFAULT FALSE;

-- 3. Dim Customers
CREATE TABLE IF NOT EXISTS customers.dim_customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) DEFAULT 'Amazon Customer',
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    customer_segment VARCHAR(50) NOT NULL DEFAULT 'Prime',
    shipping_address TEXT DEFAULT '221B Baker Street, Apt 4B',
    city VARCHAR(100) DEFAULT 'Seattle',
    postal_code VARCHAR(20) DEFAULT '98101',
    signup_date DATE NOT NULL DEFAULT CURRENT_DATE,
    country_code VARCHAR(10) NOT NULL DEFAULT 'US'
);

ALTER TABLE customers.dim_customers ADD COLUMN IF NOT EXISTS name VARCHAR(100) DEFAULT 'Amazon Customer';
ALTER TABLE customers.dim_customers ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);
ALTER TABLE customers.dim_customers ADD COLUMN IF NOT EXISTS shipping_address TEXT DEFAULT '221B Baker Street, Apt 4B';
ALTER TABLE customers.dim_customers ADD COLUMN IF NOT EXISTS city VARCHAR(100) DEFAULT 'Seattle';
ALTER TABLE customers.dim_customers ADD COLUMN IF NOT EXISTS postal_code VARCHAR(20) DEFAULT '98101';

-- 4. Dim Fulfillment Centers
CREATE TABLE IF NOT EXISTS fulfillment.dim_fulfillment_centers (
    fulfillment_center_id VARCHAR(10) PRIMARY KEY,
    fc_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL
);

-- 5. Fact Glance Views
CREATE TABLE IF NOT EXISTS retail_traffic.fact_glance_views (
    view_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asin VARCHAR(10) NOT NULL,
    customer_id INT NOT NULL,
    view_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    device_type VARCHAR(20) NOT NULL,
    is_buy_box_winner BOOLEAN NOT NULL,
    estimated_delivery_days INT NOT NULL CHECK (estimated_delivery_days >= 0),
    CONSTRAINT fk_fact_glance_views_product
        FOREIGN KEY (asin) REFERENCES catalog.dim_products(asin),
    CONSTRAINT fk_fact_glance_views_customer
        FOREIGN KEY (customer_id) REFERENCES customers.dim_customers(customer_id)
);

-- 6. Fact Orders
CREATE TABLE IF NOT EXISTS retail_sales.fact_orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id INT NOT NULL REFERENCES customers.dim_customers(customer_id),
    order_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(50) NOT NULL,
    order_status VARCHAR(20) NOT NULL DEFAULT 'Completed',
    shipping_name VARCHAR(100),
    shipping_address TEXT,
    shipping_city VARCHAR(100),
    shipping_postal_code VARCHAR(20),
    total_amount NUMERIC(10, 2) DEFAULT 0,
    delivery_estimate_date DATE,
    tracking_number VARCHAR(50)
);

ALTER TABLE retail_sales.fact_orders ADD COLUMN IF NOT EXISTS shipping_name VARCHAR(100);
ALTER TABLE retail_sales.fact_orders ADD COLUMN IF NOT EXISTS shipping_address TEXT;
ALTER TABLE retail_sales.fact_orders ADD COLUMN IF NOT EXISTS shipping_city VARCHAR(100);
ALTER TABLE retail_sales.fact_orders ADD COLUMN IF NOT EXISTS shipping_postal_code VARCHAR(20);
ALTER TABLE retail_sales.fact_orders ADD COLUMN IF NOT EXISTS total_amount NUMERIC(10, 2) DEFAULT 0;
ALTER TABLE retail_sales.fact_orders ADD COLUMN IF NOT EXISTS delivery_estimate_date DATE;
ALTER TABLE retail_sales.fact_orders ADD COLUMN IF NOT EXISTS tracking_number VARCHAR(50);

-- 7. Fact Order Items
CREATE TABLE IF NOT EXISTS retail_sales.fact_order_items (
    order_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES retail_sales.fact_orders(order_id) ON DELETE CASCADE,
    asin VARCHAR(10) NOT NULL REFERENCES catalog.dim_products(asin),
    ordered_units INT NOT NULL CHECK (ordered_units > 0),
    item_price NUMERIC(10, 2) NOT NULL CHECK (item_price >= 0),
    net_revenue NUMERIC(10, 2) NOT NULL CHECK (net_revenue >= 0)
);

-- 8. Fact FBA Inventory Daily
CREATE TABLE IF NOT EXISTS retail_inventory.fact_fba_inventory_daily (
    snapshot_date DATE NOT NULL,
    asin VARCHAR(10) NOT NULL,
    fulfillment_center_id VARCHAR(10) NOT NULL,
    units_in_stock INT NOT NULL CHECK (units_in_stock >= 0),
    units_reserved INT NOT NULL DEFAULT 0 CHECK (units_reserved >= 0),
    out_of_stock_flag BOOLEAN NOT NULL,
    PRIMARY KEY (snapshot_date, asin, fulfillment_center_id),
    CONSTRAINT fk_fact_inventory_product
        FOREIGN KEY (asin) REFERENCES catalog.dim_products(asin),
    CONSTRAINT fk_fact_inventory_fulfillment_center
        FOREIGN KEY (fulfillment_center_id)
        REFERENCES fulfillment.dim_fulfillment_centers(fulfillment_center_id)
);

-- 9. Cart Items
CREATE TABLE IF NOT EXISTS customers.cart_items (
    cart_item_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers.dim_customers(customer_id) ON DELETE CASCADE,
    asin VARCHAR(10) NOT NULL REFERENCES catalog.dim_products(asin) ON DELETE CASCADE,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    is_saved_for_later BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_cart_customer_asin_saved UNIQUE (customer_id, asin, is_saved_for_later)
);

-- 10. Wishlists
CREATE TABLE IF NOT EXISTS customers.wishlists (
    wishlist_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers.dim_customers(customer_id) ON DELETE CASCADE,
    asin VARCHAR(10) NOT NULL REFERENCES catalog.dim_products(asin) ON DELETE CASCADE,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_wishlist_customer_asin UNIQUE (customer_id, asin)
);

-- 11. Customer Reviews
CREATE TABLE IF NOT EXISTS catalog.dim_reviews (
    review_id SERIAL PRIMARY KEY,
    asin VARCHAR(10) NOT NULL REFERENCES catalog.dim_products(asin) ON DELETE CASCADE,
    customer_id INT NOT NULL REFERENCES customers.dim_customers(customer_id) ON DELETE CASCADE,
    customer_name VARCHAR(100) NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_title VARCHAR(255) NOT NULL,
    review_text TEXT NOT NULL,
    is_verified_purchase BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lightning fast queries
CREATE INDEX IF NOT EXISTS idx_products_category ON catalog.dim_products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_brand ON catalog.dim_products(brand);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON retail_sales.fact_orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_cart_customer ON customers.cart_items(customer_id);
CREATE INDEX IF NOT EXISTS idx_wishlist_customer ON customers.wishlists(customer_id);
CREATE INDEX IF NOT EXISTS idx_reviews_asin ON catalog.dim_reviews(asin);
