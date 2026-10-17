# Amazon Clone | Full-Stack Storefront & Product Analytics

A full-stack e-commerce learning project that combines an interactive Amazon-inspired storefront with a PostgreSQL-backed product catalog and a separate Python analytics workflow. The project demonstrates how application data can be extracted into CSV, explored with Pandas, segmented into business groups, and presented as visual reports.

> **Portfolio/demo project:** this is an independent educational project and is not affiliated with Amazon. The review records in the included analytics sample are synthetic demo data, not verified customer feedback.

## Project at a glance

| Layer | Technology | Purpose |
|---|---|---|
| Storefront | HTML, CSS, JavaScript | Responsive shopping experience and interactive catalog |
| Web application | Python, Flask | Store pages, APIs, sessions, authentication, cart, wishlist, and checkout |
| Database | PostgreSQL on Neon | Persistent catalog, customer, traffic, review, inventory, and order data |
| Analytics | Python, Pandas, Matplotlib | CSV extraction, data-quality checks, EDA, portfolio segmentation, and charts |

## Storefront capabilities

- Search, autocomplete, category filters, sorting, and product detail views
- Product ratings, customer reviews, and review submission
- Session-aware account flows, demo account, cart, saved items, and wishlist
- Checkout, delivery options, order history, and package tracking
- Customer support interface and responsive storefront layout

## Application and analytics data flow

The web application and the analytics workflow use the same Neon database for different purposes:

```text
Browser
  │  HTTP requests
  ▼
Flask application (app.py)
  │  parameterized PostgreSQL queries
  ▼
Neon PostgreSQL ───────────────────────────────────────┐
  │                                                    │
  │ analytics export scripts                           │ storefront reads/writes
  ▼                                                    │
data/raw/product_views_analysis.csv                    │
  │                                                    │
  ├── Pandas EDA: quality, distributions, outliers     │
  ├── portfolio gates: rating ≥ 4.2, views ≥ 20        │
  └── processed CSVs + Matplotlib PNG charts           │
                                                       ▼
                                                Storefront APIs
```

The raw product CSV is an analytics snapshot, not the application's live database. The export script aggregates catalog products with glance-view traffic. The review export joins product, traffic, and review data to produce an at-risk review extract. Pandas reads these CSV snapshots for repeatable analysis; segmentation and chart scripts then write derived datasets and images to their own folders.

The current sample contains **79 products** and the following fields in the raw product export: `asin`, `product_title`, `total_views`, `average_rating`, and `standard_price`. The sample review export is synthetic and should be treated as demonstration data only.

### Analytics visuals

All generated charts are saved in [`reports/visualisations/`](reports/visualisations/).

#### Portfolio segmentation

Products are grouped using two explicit gates: high rating is **≥ 4.2** and high traffic is **≥ 20 views**.

![Product portfolio segmentation matrix](reports/visualisations/SEGMENTATION.png)

#### Traffic distribution and outlier check

The boxplot applies the 1.5×IQR outlier rule. The histogram zooms into the 0–100-view range so the bulk of products is visible beside high-traffic outliers.

![Product views boxplot](reports/visualisations/product_views_boxplot.png)

![Product views distribution](reports/visualisations/product_views_distribution.png)

#### Price, traffic, and rating relationships

The correlation heatmap and scatter plot summarize linear association in this dataset; correlation is descriptive and does not imply causation.

![Product metric correlation heatmap](reports/visualisations/product_metrics_correlation.png)

![Product price versus views](reports/visualisations/product_price_vs_views.png)

See the [executive EDA report](reports/PROJECT_SUMMARY_REPORT.md) for findings, segment counts, review-audit caveats, and recommended actions.

## Database overview

The schema is defined in [`schema.sql`](schema.sql). The application and analysis scripts use these logical areas:

| Schema | Example tables | Role |
|---|---|---|
| `catalog` | `dim_products`, `dim_categories`, `dim_reviews` | Product catalog, categories, and reviews |
| `customers` | `dim_customers`, `cart_items`, `wishlists` | Customer profiles and shopping state |
| `retail_traffic` | `fact_glance_views` | Product traffic events used in analytics |
| `retail_inventory` | `fact_fba_inventory_daily` | Inventory availability |
| `retail_sales` | `fact_orders`, `fact_order_items` | Order and line-item records |
| `fulfillment` | `dim_fulfillment_centers` | Fulfillment center reference data |

## Repository layout

```text
.
├── app.py                         # Flask application
├── templates/
│   └── index.html                 # Storefront UI
├── data/
│   ├── raw/                       # Source analytics CSV snapshot
│   └── processed/                 # Segmentation and review CSV outputs
├── eda/
│   ├── visualisations/            # Chart-generation scripts
│   └── *.py                       # EDA, exports, and portfolio analysis
├── reports/
│   ├── visualisations/            # Generated PNG charts embedded above
│   └── PROJECT_SUMMARY_REPORT.md  # Executive analysis report
├── schema.sql                     # PostgreSQL DDL
├── seed_data.py                  # Demo database seeding
├── requirements.txt              # Storefront dependencies
└── requirements-eda.txt          # Analytics dependencies
```

## Local setup

### 1. Requirements

- Python 3.10 or newer
- A PostgreSQL database (Neon is used by the hosted demo)
- Optional: `psql` to initialize the schema from the command line

### 2. Install dependencies and configure environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -r requirements-eda.txt
Copy-Item .env.example .env
```

Edit `.env` and set your own values:

```dotenv
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
FLASK_SECRET_KEY=replace-with-a-long-random-secret
FLASK_DEBUG=false
```

Generate a session secret with:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Keep real credentials in `.env` or the hosting provider's secret manager. **Never commit `.env` or put real connection strings in Python, notebooks, screenshots, or documentation.** The repository ignores `.env`; `.env.example` contains placeholders only.

### 3. Initialize and seed the database

Create the database tables using [`schema.sql`](schema.sql), then load demo records with [`seed_data.py`](seed_data.py). Both use the `DATABASE_URL` from `.env`. Run these only against a development database you control.

```powershell
psql $env:DATABASE_URL -f schema.sql
python seed_data.py
```

### 4. Start the web application

```powershell
python app.py
```

Open <http://127.0.0.1:5000>.

### 5. Run the analytics workflow

The EDA scripts use paths relative to the repository, so run from the project root. The database export steps are optional if you want to use the included CSV snapshots.

```powershell
# Optional: refresh the raw product/traffic snapshot from Neon
python eda/export_product_views.py

# Inspect, validate, and segment the CSV snapshot
python eda/01_data_understanding.py
python eda/02_data_quality.py
python eda/03_univariate_analysis.py
python eda/05_actionable_insights.py
python eda/find_at_risk.py

# Optional: export the at-risk product review sample from Neon
python eda/export_reviews_analysis.py
python eda/low_rated_reviews.py

# Generate all PNG charts
python eda/visualisations/boxplots.py
python eda/visualisations/distributions.py
python eda/visualisations/ratings_analysis.py
python eda/visualisations/views_vs_price.py
python eda/segmentation.py
```

Outputs:

- Raw product snapshot: `data/raw/product_views_analysis.csv`
- Segmentation and review extracts: `data/processed/`
- Generated chart images: `reports/visualisations/`

### 6. Tests

```powershell
python test_suite.py
```

The integration tests require the database to be configured and seeded.

## Deployment preparation

The app is structured for a Flask deployment and has previously been hosted on Vercel. Before deploying a fresh environment:

1. Create/configure the PostgreSQL database and apply `schema.sql`.
2. Configure `DATABASE_URL` and a strong, unique `FLASK_SECRET_KEY` in the host's production environment settings.
3. Confirm the required database tables and demo/catalog records exist.
4. Deploy from the GitHub repository and verify the production build and database connectivity in the host's logs.

Do not commit environment secrets. The analytics CSV snapshots and report images are committed as project/demo assets; refresh them only from a database you are authorized to query.

## License and attribution

This repository is an educational Amazon-inspired clone. Amazon and related marks belong to their respective owners. Add a license before reusing or distributing the code if a specific license is intended.
