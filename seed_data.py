import json
import os
import random
from datetime import date, datetime, timedelta
import psycopg2
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Predefined realistic Amazon catalog items across 6 departments
CATEGORIES = [
    {"name": "Smartphones", "department": "Electronics", "icon": "fa-mobile-screen"},
    {"name": "Headphones & Audio", "department": "Electronics", "icon": "fa-headphones"},
    {"name": "Laptops & Tablets", "department": "Computers", "icon": "fa-laptop"},
    {"name": "Computer Accessories", "department": "Computers", "icon": "fa-keyboard"},
    {"name": "Kitchen Appliances", "department": "Home & Kitchen", "icon": "fa-blender"},
    {"name": "Home Decor & Cleaning", "department": "Home & Kitchen", "icon": "fa-couch"},
    {"name": "Footwear & Shoes", "department": "Fashion", "icon": "fa-shoe-prints"},
    {"name": "Watches & Accessories", "department": "Fashion", "icon": "fa-clock"},
    {"name": "Books & Audiobooks", "department": "Books", "icon": "fa-book"},
    {"name": "Personal Care & Beauty", "department": "Beauty & Personal Care", "icon": "fa-spa"},
]

PRODUCTS_DATA = [
    # Electronics - Smartphones
    {
        "asin": "B0CHX1W1XY",
        "title": "Apple iPhone 15 Pro Max (256 GB) - Natural Titanium",
        "brand": "Apple",
        "category": "Smartphones",
        "department": "Electronics",
        "price": 1199.99,
        "original_price": 1299.99,
        "discount_percent": 8,
        "rating": 4.8,
        "rating_count": 14230,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": False,
        "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=700&q=80",
            "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=700&q=80",
            "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "iPhone 15 Pro Max. Forged in titanium and featuring the groundbreaking A17 Pro chip, a customizable Action button, and the most powerful iPhone camera system ever.",
        "features": [
            "FORGED IN TITANIUM — iPhone 15 Pro Max has a strong and light aerospace-grade titanium design with a textured matte-glass back.",
            "ADVANCED DISPLAY — The 6.7” Super Retina XDR display with ProMotion ramps up refresh rates to 120Hz.",
            "GAME-CHANGING A17 PRO CHIP — A Pro-class GPU makes mobile games feel so immersive, with rich environments and realistic characters.",
            "POWERFUL PRO CAMERA SYSTEM — 7 pro lenses of tremendous framing flexibility. Capture super-high-resolution photos with the 48MP Main camera.",
            "ACTION BUTTON — A fast track to your favorite feature. Set Silent mode, Camera, Voice Memo, Shortcut, and more."
        ]
    },
    {
        "asin": "B0CMZ6PZ3G",
        "title": "Samsung Galaxy S24 Ultra AI Smartphone (512GB, Titanium Gray)",
        "brand": "Samsung",
        "category": "Smartphones",
        "department": "Electronics",
        "price": 1249.99,
        "original_price": 1419.99,
        "discount_percent": 12,
        "rating": 4.7,
        "rating_count": 8750,
        "is_prime": True,
        "is_best_seller": False,
        "is_amazons_choice": True,
        "image_url": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=700&q=80",
            "https://images.unsplash.com/photo-1580910051074-3eb694886505?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Meet Galaxy S24 Ultra, the ultimate form of Galaxy Ultra with a new titanium exterior and a 6.8-inch flat display. It is an absolute marvel of design.",
        "features": [
            "CIRCLE TO SEARCH — Search like never before with Circle to Search with Google. Simply trace an object to get Google Search results.",
            "LIVE TRANSLATE — Speak foreign languages on the spot with Live Translate during phone calls.",
            "200MP CAMERA — Meet the industry standard for camera quality with the most mega pixels on a smartphone.",
            "NOTE ASSIST — Summarize, format and translate your notes with Galaxy AI.",
            "BUILT-IN S PEN — The legacy of Galaxy Note is alive and well. Write, tap and navigate with precision."
        ]
    },
    {
        "asin": "B0BMWHBL77",
        "title": "Google Pixel 8 Pro - Unlocked Android Smartphone with Telephoto Lens (Obsidian)",
        "brand": "Google",
        "category": "Smartphones",
        "department": "Electronics",
        "price": 799.00,
        "original_price": 999.00,
        "discount_percent": 20,
        "rating": 4.6,
        "rating_count": 5120,
        "is_prime": True,
        "is_best_seller": False,
        "is_amazons_choice": False,
        "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Pixel 8 Pro is the all-pro phone engineered by Google; it’s super fast, personal, and helpful, with a sophisticated design.",
        "features": [
            "GOOGLE TENSOR G3 — Google's most powerful chip yet, making Pixel 8 Pro fast and efficient.",
            "IMMERSIVE 6.7-INCH DISPLAY — Super Actua display makes everything look sharp and vibrant.",
            "TEMPERATURE SENSOR — Quickly check body temperature and object warmth.",
            "NEXT-GEN TRIPLE CAMERA — 50MP main camera with 5x optical zoom."
        ]
    },

    # Electronics - Headphones & Audio
    {
        "asin": "B09XS7JWHH",
        "title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones - Black",
        "brand": "Sony",
        "category": "Headphones & Audio",
        "department": "Electronics",
        "price": 348.00,
        "original_price": 399.99,
        "discount_percent": 13,
        "rating": 4.7,
        "rating_count": 22450,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": True,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=700&q=80",
            "https://images.unsplash.com/photo-1484704849700-f032a568e944?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "The WH-1000XM5 headphones rewrite the rules for distraction-free listening. Two processors control 8 microphones for unprecedented noise cancellation.",
        "features": [
            "INDUSTRY-LEADING NOISE CANCELING — Two processors control 8 microphones for unprecedented noise cancellation.",
            "MAGNIFICENT SOUND — Engineered to perfection with the new Integrated Processor V1.",
            "CRYSTAL CLEAR CALLS — 4 beamforming microphones with AI noise reduction.",
            "UP TO 30-HOUR BATTERY LIFE — Quick 3-minute charging gives 3 hours of playback.",
            "ULTRA-COMFORTABLE DESIGN — Lightweight design with soft fit leather."
        ]
    },
    {
        "asin": "B0D1XD1ZW3",
        "title": "Apple AirPods Pro (2nd Generation) Wireless Earbuds with USB-C Charging",
        "brand": "Apple",
        "category": "Headphones & Audio",
        "department": "Electronics",
        "price": 189.99,
        "original_price": 249.00,
        "discount_percent": 24,
        "rating": 4.8,
        "rating_count": 48900,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": False,
        "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "AirPods Pro feature up to 2x more Active Noise Cancellation, plus Adaptive Audio and Transparency mode, which lets you hear the world around you.",
        "features": [
            "PIONEERING AUDIO — The Apple-designed H2 chip pushes advanced audio performance further.",
            "NEXT-LEVEL ACTIVE NOISE CANCELLATION — Up to 2x more noise reduction than previous gen.",
            "CUSTOMIZABLE FIT — Includes 4 pairs of silicone tips (XS, S, M, L).",
            "DUST, SWEAT, AND WATER RESISTANT — Both AirPods Pro and the MagSafe Charging Case are IP54 rated."
        ]
    },

    # Computers - Laptops & Tablets
    {
        "asin": "B0CX23V25K",
        "title": "Apple 2024 MacBook Air 15-inch Laptop with M3 chip (16GB RAM, 512GB SSD) - Space Gray",
        "brand": "Apple",
        "category": "Laptops & Tablets",
        "department": "Computers",
        "price": 1499.00,
        "original_price": 1699.00,
        "discount_percent": 12,
        "rating": 4.9,
        "rating_count": 3410,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": True,
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=700&q=80",
            "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "The M3 chip brings even greater capabilities to the superportable 15-inch MacBook Air. With up to 18 hours of battery life, you can take it anywhere and blaze through work and play.",
        "features": [
            "LEAN. MEAN. M3 MACHINE — The incredibly thin and fast MacBook Air sails through work and play.",
            "PORTABLE DESIGN — Lightweight and under half an inch thin.",
            "GET MORE DONE FASTER — Powerful 8-core CPU and 10-core GPU in the Apple M3 chip.",
            "UP TO 18 HOURS BATTERY — Phenomenal, all-day battery life.",
            "A BRILLIANT DISPLAY — 15.3-inch Liquid Retina display supports 1 billion colors."
        ]
    },
    {
        "asin": "B0CD9F23X4",
        "title": "Dell XPS 13 9315 Thin & Light Laptop (Intel i7-1250U, 16GB RAM, 512GB SSD, FHD+ Display)",
        "brand": "Dell",
        "category": "Laptops & Tablets",
        "department": "Computers",
        "price": 899.99,
        "original_price": 1099.99,
        "discount_percent": 18,
        "rating": 4.4,
        "rating_count": 1890,
        "is_prime": True,
        "is_best_seller": False,
        "is_amazons_choice": False,
        "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Dell XPS 13 is lightweight, durable and beautifully designed from CNC machined aluminum. Experience vivid colors on the InfinityEdge borderless display.",
        "features": [
            "INFINITYEDGE DISPLAY — 13.4-inch FHD+ borderless screen with high brightness.",
            "ULTRA-PORTABLE — Weighs only 2.59 lbs with sleek 0.55-inch profile.",
            "POWERFUL PERFORMANCE — 12th Gen Intel Core i7 with Intel Iris Xe Graphics.",
            "EXPRESSCHARGE — Charge up to 80% battery in under an hour."
        ]
    },

    # Computers - Accessories
    {
        "asin": "B07S395RWD",
        "title": "Logitech MX Master 3S Wireless Performance Mouse with Quiet Clicks & 8K DPI Sensor",
        "brand": "Logitech",
        "category": "Computer Accessories",
        "department": "Computers",
        "price": 99.99,
        "original_price": 119.99,
        "discount_percent": 17,
        "rating": 4.8,
        "rating_count": 38900,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": True,
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Meet MX Master 3S – an iconic mouse remastered. Feel every moment of your workflow with even more precision, tactility, and performance, thanks to Quiet Clicks and an 8,000 DPI track-on-glass sensor.",
        "features": [
            "QUIET CLICKS — 90% less click noise with identical satisfying click feel.",
            "8K DPI ANY-SURFACE TRACKING — Works seamlessly even on glass.",
            "MAGSPEED SCROLLING — Scroll 1,000 lines in 1 second with ultra-quiet precision.",
            "MULTI-DEVICE FLOW — Pair with up to 3 computers across Windows, macOS, and Linux.",
            "USB-C FAST CHARGING — Full charge lasts up to 70 days."
        ]
    },
    {
        "asin": "B09V7N8G6P",
        "title": "Keychron K2 Version 2 Wireless Mechanical Keyboard (RGB Backlight, Gateron Brown Switches)",
        "brand": "Keychron",
        "category": "Computer Accessories",
        "department": "Computers",
        "price": 79.99,
        "original_price": 99.00,
        "discount_percent": 19,
        "rating": 4.7,
        "rating_count": 7820,
        "is_prime": True,
        "is_best_seller": False,
        "is_amazons_choice": False,
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "A 75% layout wireless mechanical keyboard compatible with Mac and Windows. Connects up to 3 devices via Bluetooth or wired USB Type-C.",
        "features": [
            "DUAL MODE CONNECTIVITY — Bluetooth 5.1 and wired Type-C connection.",
            "MAC & WINDOWS COMPATIBILITY — Unique Mac layout with full Mac media keys.",
            "TACTILE GATERON SWITCHES — Rated for 50 million keystrokes.",
            "LONG BATTERY LIFE — 4000 mAh rechargeable battery gives up to 72 hours typing."
        ]
    },

    # Home & Kitchen - Kitchen Appliances
    {
        "asin": "B07FDJMC9Q",
        "title": "Ninja AF101 Air Fryer that Crisps, Roasts, Reheats & Dehydrates (4-Quart, High Gloss Finish)",
        "brand": "Ninja",
        "category": "Kitchen Appliances",
        "department": "Home & Kitchen",
        "price": 89.99,
        "original_price": 129.99,
        "discount_percent": 31,
        "rating": 4.8,
        "rating_count": 61200,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": True,
        "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Now enjoy guilt-free food with Ninja Air Fryer. Air fry with up to 75 percent less fat than traditional frying methods.",
        "features": [
            "GUILT-FREE FRIED FOOD — Air fry with up to 75% less fat than traditional frying.",
            "WIDE TEMPERATURE RANGE — 105°F to 400°F allows gentle dehydrating to flash crisping.",
            "4-QUART CERAMIC BASKET — Fits up to 2 lbs of french fries.",
            "DISHWASHER SAFE PARTS — Easy cleanup with nonstick basket and crisper plate."
        ]
    },
    {
        "asin": "B01N0UB7C1",
        "title": "Nespresso VertuoPlus Coffee and Espresso Maker by De'Longhi (Matte Black)",
        "brand": "Nespresso",
        "category": "Kitchen Appliances",
        "department": "Home & Kitchen",
        "price": 149.95,
        "original_price": 199.00,
        "discount_percent": 25,
        "rating": 4.6,
        "rating_count": 21300,
        "is_prime": True,
        "is_best_seller": False,
        "is_amazons_choice": False,
        "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Nespresso VertuoPlus coffee and espresso machine brews 4 single-serve cup sizes at the touch of a button using patented Centrifusion technology.",
        "features": [
            "VERSATILE BREWING — Brews 5 oz and 7.77 oz Coffee, and single and double Espresso.",
            "CENTRIFUSION TECHNOLOGY — Spins capsule up to 7,000 rotations per minute for crema perfection.",
            "ONE-TOUCH OPERATION — Fast heat up in just 20-25 seconds with motorized head.",
            "EXTRA LARGE WATER TANK — 60 oz movable water tank to fit kitchen counter space."
        ]
    },

    # Home & Kitchen - Home Decor & Cleaning
    {
        "asin": "B0892B3Q4X",
        "title": "Dyson V12 Detect Slim Cordless Vacuum Cleaner with Laser Dirt Illumination",
        "brand": "Dyson",
        "category": "Home Decor & Cleaning",
        "department": "Home & Kitchen",
        "price": 549.99,
        "original_price": 649.99,
        "discount_percent": 15,
        "rating": 4.6,
        "rating_count": 4200,
        "is_prime": True,
        "is_best_seller": False,
        "is_amazons_choice": True,
        "image_url": "https://images.unsplash.com/photo-1558317374-067fb5f30001?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1558317374-067fb5f30001?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Dyson's lightest intelligent cordless vacuum. Engineered for whole-home deep cleaning with laser illumination that reveals invisible dust on hard floors.",
        "features": [
            "LASER SLIM FLUFFY CLEANER HEAD — Reveals invisible dust on hard floors.",
            "PIEZO SENSOR & LCD SCREEN — Continuously sizes and counts dust particles.",
            "UP TO 60 MINUTES RUN TIME — High power fade-free lithium-ion battery.",
            "HAIR SCREW TOOL — Anti-tangle conical brush bar clears pet hair quickly."
        ]
    },

    # Fashion - Footwear & Shoes
    {
        "asin": "B08F9T6K3Z",
        "title": "Nike Men's Air Max 270 Athletic Running Sneakers (Triple Black)",
        "brand": "Nike",
        "category": "Footwear & Shoes",
        "department": "Fashion",
        "price": 159.95,
        "original_price": 179.99,
        "discount_percent": 11,
        "rating": 4.7,
        "rating_count": 18400,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": False,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=700&q=80",
            "https://images.unsplash.com/photo-1552346154-21d32810aba3?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Boasting Nike's biggest heel Air unit yet, the Nike Air Max 270 delivers unrivaled, all-day comfort with sleek, running-inspired styling.",
        "features": [
            "MAX AIR 270 HEEL UNIT — Delivers unrivaled, all-day comfort and responsiveness.",
            "BREATHABLE MESH UPPER — Woven synthetic fabric provides a lightweight, airy feel.",
            "STRETCHY INNER SLEEVE — Creates a personalized sock-like fit.",
            "RUBBER OUTSOLE — Superior traction and durable grip on diverse surfaces."
        ]
    },
    {
        "asin": "B079DGMKLR",
        "title": "Levi's Men's 501 Original Fit Jeans (Medium Stonewash)",
        "brand": "Levi's",
        "category": "Footwear & Shoes",
        "department": "Fashion",
        "price": 59.99,
        "original_price": 79.50,
        "discount_percent": 25,
        "rating": 4.5,
        "rating_count": 31200,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": True,
        "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Since we invented it in 1873, the 501 Jean has been a blank canvas for self-expression. Straight fit with signature button fly.",
        "features": [
            "100% COTTON DENIM — Non-stretch authentic heritage denim.",
            "ORIGINAL STRAIGHT FIT — Sits at waist with straight leg styling.",
            "SIGNATURE BUTTON FLY — The timeless classic button closure.",
            "MACHINE WASHABLE — Crafted for decades of everyday wear."
        ]
    },

    # Fashion - Watches & Accessories
    {
        "asin": "B000GAYQL8",
        "title": "Casio Vintage Digital Chronograph Stainless Steel Watch (A168WA-1YES)",
        "brand": "Casio",
        "category": "Watches & Accessories",
        "department": "Fashion",
        "price": 27.95,
        "original_price": 35.00,
        "discount_percent": 20,
        "rating": 4.7,
        "rating_count": 27800,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": True,
        "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "A retro-inspired digital watch with electro-luminescent backlight, 1/100-second stopwatch, daily alarm, and auto-calendar.",
        "features": [
            "RETRO ICONIC LOOK — Stainless steel link bracelet with adjustable folding clasp.",
            "EL BACKLIGHT — Illuminator backlight for crystal-clear night viewing.",
            "CHRONOGRAPH & ALARM — 1/100 second stopwatch and daily alarm alerts.",
            "WATER RESISTANT — Resists splashes and rain."
        ]
    },

    # Books - Best Sellers
    {
        "asin": "B07D23CFGR",
        "title": "Atomic Habits: An Easy & Proven Way to Build Good Habits & Break Bad Ones (Hardcover)",
        "brand": "James Clear",
        "category": "Books & Audiobooks",
        "department": "Books",
        "price": 14.99,
        "original_price": 27.00,
        "discount_percent": 44,
        "rating": 4.9,
        "rating_count": 125000,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": True,
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Over 15 million copies sold! No matter your goals, Atomic Habits offers a proven framework for improving every day. James Clear reveals practical strategies to master tiny behaviors that lead to remarkable results.",
        "features": [
            "#1 NEW YORK TIMES BESTSELLER — Translated into over 50 languages worldwide.",
            "PRACTICAL HABIT LOOP — Learn the Cue, Craving, Response, and Reward system.",
            "IDENTITY-BASED CHANGE — Make good habits inevitable and bad habits impossible.",
            "PREMIUM HARDCOVER EDITION — Printed on acid-free archival quality paper."
        ]
    },
    {
        "asin": "B084G4MG28",
        "title": "The Psychology of Money: Timeless lessons on wealth, greed, and happiness",
        "brand": "Morgan Housel",
        "category": "Books & Audiobooks",
        "department": "Books",
        "price": 13.49,
        "original_price": 19.99,
        "discount_percent": 33,
        "rating": 4.8,
        "rating_count": 54000,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": False,
        "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Doing well with money isn’t necessarily about what you know. It’s about how you behave. And behavior is hard to teach, even to really smart people.",
        "features": [
            "19 SHORT STORIES — Explores the strange ways people think about money.",
            "TIMELESS PERSPECTIVE — Master financial decision making in volatile worlds.",
            "PRAISED BY EXPERTS — Wall Street Journal and Financial Times recommended."
        ]
    },

    # Beauty & Personal Care
    {
        "asin": "B01N4EWVEE",
        "title": "CeraVe Hydrating Facial Cleanser with Hyaluronic Acid & Ceramides (16 Fl Oz)",
        "brand": "CeraVe",
        "category": "Personal Care & Beauty",
        "department": "Beauty & Personal Care",
        "price": 15.48,
        "original_price": 17.99,
        "discount_percent": 14,
        "rating": 4.7,
        "rating_count": 94000,
        "is_prime": True,
        "is_best_seller": True,
        "is_amazons_choice": True,
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Developed with dermatologists, CeraVe Hydrating Cleanser is a gentle face wash with ingredients like ceramides and hyaluronic acid that work to restore the skin’s natural barrier.",
        "features": [
            "DAILY FACE WASH — Cleanses and refreshes without over-stripping moisture.",
            "ESSENTIAL CERAMIDES — Formulated with three essential ceramides (1, 3, 6-II).",
            "NON-FOAMING LOTION FORMULA — Removes dirt and makeup while hydrating skin.",
            "DERMATOLOGIST RECOMMENDED — Fragrance-free, paraben-free, and non-comedogenic."
        ]
    },
    {
        "asin": "B08DNK25G2",
        "title": "Philips Sonicare ProtectiveClean 4100 Rechargeable Electric Toothbrush (Deep Black)",
        "brand": "Philips Sonicare",
        "category": "Personal Care & Beauty",
        "department": "Beauty & Personal Care",
        "price": 49.96,
        "original_price": 69.96,
        "discount_percent": 29,
        "rating": 4.7,
        "rating_count": 48200,
        "is_prime": True,
        "is_best_seller": False,
        "is_amazons_choice": True,
        "image_url": "https://images.unsplash.com/photo-1559591937-e62fb330bc1f?auto=format&fit=crop&w=700&q=80",
        "additional_images": [
            "https://images.unsplash.com/photo-1559591937-e62fb330bc1f?auto=format&fit=crop&w=700&q=80"
        ],
        "description": "Removes up to 7x more plaque than a manual toothbrush. Pressure sensor protects teeth and gums from excess brushing pressure.",
        "features": [
            "PRESSURE SENSOR — Alerts you when brushing too hard to safeguard enamel.",
            "BRUSHSYNC TECHNOLOGY — Tracks how long you've been using your brush head.",
            "QUADPACER & SMARTIMER — Encourages attentive 2-minute brushing habit.",
            "BATTERY CHARGE INDICATOR — Up to 14 days of power between charges."
        ]
    }
]

REVIEWS_SEED = [
    {
        "rating": 5,
        "author": "David K.",
        "title": "Outstanding build quality and battery life!",
        "text": "I upgraded after 3 years and the difference is night and day. Premium materials, flawless performance, and arrives in classic Amazon Prime 1-day shipping. Highly recommended!"
    },
    {
        "rating": 5,
        "author": "Sarah Jenkins",
        "title": "Exceeded all my expectations! Must buy.",
        "text": "Looks and feels amazing. Does everything advertised with speed and precision. Very satisfied with this purchase!"
    },
    {
        "rating": 4,
        "author": "Michael Chang",
        "title": "Great value, minor learning curve",
        "text": "Very happy with the overall product. Solid packaging and great features. Giving 4 stars only because setup took a few minutes, but afterwards it runs like a dream."
    },
    {
        "rating": 5,
        "author": "Emily R.",
        "title": "Legit 5 stars - will definitely buy again",
        "text": "I was hesitant at first but this is top-notch. Truly authentic quality and works seamlessly every day."
    }
]

DEMO_CUSTOMER = {
    "name": "Alex Mercer",
    "email": "demo@amazon-clone.local",
    "password": "amazonpassword123",
    "shipping_address": "410 Terry Ave N",
    "city": "Seattle",
    "postal_code": "98109"
}

FULFILLMENT_CENTER = {
    "id": "FC-SEA1",
    "name": "Amazon Fulfillment Center SEA1",
    "city": "Seattle",
    "state": "WA",
    "country": "US"
}


def seed_database():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL not set in .env")

    print(f"Connecting to Neon PostgreSQL...")
    conn = psycopg2.connect(db_url, sslmode="require")
    cur = conn.cursor()

    try:
        print("1. Inserting fulfillment center...", flush=True)
        cur.execute("""
            INSERT INTO fulfillment.dim_fulfillment_centers (fulfillment_center_id, fc_name, city, state, country)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (fulfillment_center_id) DO UPDATE SET
                fc_name = EXCLUDED.fc_name,
                city = EXCLUDED.city,
                state = EXCLUDED.state,
                country = EXCLUDED.country
        """, (FULFILLMENT_CENTER["id"], FULFILLMENT_CENTER["name"], FULFILLMENT_CENTER["city"], FULFILLMENT_CENTER["state"], FULFILLMENT_CENTER["country"]))

        # 2. Categories
        print("2. Inserting categories...", flush=True)
        cat_map = {}
        for cat in CATEGORIES:
            cur.execute("""
                INSERT INTO catalog.dim_categories (category_name, department, icon)
                VALUES (%s, %s, %s)
                ON CONFLICT (category_name, department) DO UPDATE SET
                    icon = EXCLUDED.icon
                RETURNING category_id
            """, (cat["name"], cat["department"], cat.get("icon", "fa-tag")))
            cat_id = cur.fetchone()[0]
            cat_map[cat["name"]] = cat_id

        # 3. Demo customer
        print("3. Inserting demo customer...", flush=True)
        pwd_hash = generate_password_hash(DEMO_CUSTOMER["password"])
        cur.execute("""
            INSERT INTO customers.dim_customers (name, email, password_hash, shipping_address, city, postal_code, signup_date)
            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
            ON CONFLICT (email) DO UPDATE SET
                name = EXCLUDED.name,
                password_hash = EXCLUDED.password_hash,
                shipping_address = EXCLUDED.shipping_address,
                city = EXCLUDED.city,
                postal_code = EXCLUDED.postal_code
            RETURNING customer_id
        """, (DEMO_CUSTOMER["name"], DEMO_CUSTOMER["email"], pwd_hash, DEMO_CUSTOMER["shipping_address"], DEMO_CUSTOMER["city"], DEMO_CUSTOMER["postal_code"]))
        demo_customer_id = cur.fetchone()[0]

        # 4. Products & Inventory
        print("4. Inserting products and inventory...", flush=True)
        today = date.today()
        for p in PRODUCTS_DATA:
            cat_id = cat_map[p["category"]]
            cur.execute("""
                INSERT INTO catalog.dim_products
                    (asin, product_title, brand, category_id, standard_price, original_price,
                     discount_percent, rating, rating_count, image_url, additional_images,
                     description, features, is_prime_eligible, is_best_seller, is_amazons_choice)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (asin) DO UPDATE SET
                    product_title = EXCLUDED.product_title,
                    brand = EXCLUDED.brand,
                    category_id = EXCLUDED.category_id,
                    standard_price = EXCLUDED.standard_price,
                    original_price = EXCLUDED.original_price,
                    discount_percent = EXCLUDED.discount_percent,
                    rating = EXCLUDED.rating,
                    rating_count = EXCLUDED.rating_count,
                    image_url = EXCLUDED.image_url,
                    additional_images = EXCLUDED.additional_images,
                    description = EXCLUDED.description,
                    features = EXCLUDED.features,
                    is_prime_eligible = EXCLUDED.is_prime_eligible,
                    is_best_seller = EXCLUDED.is_best_seller,
                    is_amazons_choice = EXCLUDED.is_amazons_choice
            """, (
                p["asin"],
                p["title"],
                p["brand"],
                cat_id,
                p["price"],
                p.get("original_price", p["price"]),
                p.get("discount_percent", 0),
                p.get("rating", 4.5),
                p.get("rating_count", 150),
                p["image_url"],
                json.dumps(p.get("additional_images", [])),
                p["description"],
                json.dumps(p["features"]),
                p.get("is_prime", True),
                p.get("is_best_seller", False),
                p.get("is_amazons_choice", False)
            ))

            # Stock inventory (snapshot for today and next few days)
            cur.execute("""
                INSERT INTO retail_inventory.fact_fba_inventory_daily
                    (snapshot_date, asin, fulfillment_center_id, units_in_stock, units_reserved, out_of_stock_flag)
                VALUES (%s, %s, %s, 150, 0, FALSE)
                ON CONFLICT (snapshot_date, asin, fulfillment_center_id) DO UPDATE SET
                    units_in_stock = EXCLUDED.units_in_stock,
                    out_of_stock_flag = FALSE
            """, (today, p["asin"], FULFILLMENT_CENTER["id"]))

            # Insert sample reviews if none exist for this product
            cur.execute("SELECT COUNT(*) FROM catalog.dim_reviews WHERE asin = %s", (p["asin"],))
            if cur.fetchone()[0] == 0:
                for rev in REVIEWS_SEED:
                    cur.execute("""
                        INSERT INTO catalog.dim_reviews (asin, customer_id, customer_name, rating, review_title, review_text)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (p["asin"], demo_customer_id, rev["author"], rev["rating"], rev["title"], rev["text"]))

        # 5. Seed a demo completed past order for the demo customer to showcase "Your Orders" feature
        cur.execute("SELECT COUNT(*) FROM retail_sales.fact_orders WHERE customer_id = %s", (demo_customer_id,))
        if cur.fetchone()[0] == 0:
            order_asin = "B07S395RWD" # MX Master 3S
            order_price = 99.99
            cur.execute("""
                INSERT INTO retail_sales.fact_orders
                    (customer_id, order_timestamp, payment_method, order_status, shipping_name,
                     shipping_address, shipping_city, shipping_postal_code, total_amount,
                     delivery_estimate_date, tracking_number)
                VALUES (%s, NOW() - INTERVAL '3 days', 'Amazon Pay / Visa ending in 4242', 'Delivered',
                        %s, %s, %s, %s, %s, CURRENT_DATE - 1, 'AMZ-TRK-9824151')
                RETURNING order_id
            """, (demo_customer_id, DEMO_CUSTOMER["name"], DEMO_CUSTOMER["shipping_address"],
                  DEMO_CUSTOMER["city"], DEMO_CUSTOMER["postal_code"], order_price))
            sample_order_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO retail_sales.fact_order_items (order_id, asin, ordered_units, item_price, net_revenue)
                VALUES (%s, %s, 1, %s, %s)
            """, (sample_order_id, order_asin, order_price, order_price))

        conn.commit()
        print(f"Successfully seeded database with {len(PRODUCTS_DATA)} products and demo user/orders!")
    except Exception as e:
        conn.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    seed_database()
