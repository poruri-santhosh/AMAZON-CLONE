# Amazon Product Portfolio EDA & Optimization

**Executive summary | 17 October 2026**

## 1. Project Overview & Objective

This analysis evaluates a 79-product catalog using product-level traffic, average rating, and listed price. The objective is to identify portfolio segments, flag traffic outliers, and prioritize product-quality and listing investigations. The analysis uses Python and Pandas over `product_views_analysis.csv`, with PostgreSQL (Neon) queries used to extract product traffic and review records.

| Measure | Result |
|---|---:|
| Products in local analysis dataset | 79 |
| Fields | ASIN, product title, total views, average rating, standard price |
| Null values | 0 |
| Duplicate rows / duplicate ASINs | 0 / 0 |
| Product-level rating range | 3.5–5.0 |
| Review records in the at-risk extract | 89 |

The currency/unit for `standard_price` is not documented in the extracted dataset; price figures below are therefore shown as raw dataset values.

## 2. Exploratory Data Analysis & Outlier Detection

### Distribution summary

| Metric | Mean | Median | Standard deviation | Minimum | Maximum |
|---|---:|---:|---:|---:|---:|
| Total views | 96.34 | 33 | 439.22 | 0 | 2,803 |
| Average rating | 4.35 | 4.4 | 0.44 | 3.5 | 5.0 |
| Standard price | 8,553.01 | 2,499 | 18,334.38 | 13.49 | 84,999 |

Views are strongly right-skewed: the mean is lifted well above the median by two products with 2,803 views each. Price is also right-skewed, with a maximum far above the median. The rating distribution is concentrated toward the higher end, although the portfolio includes low-rated, high-traffic products.

The pairwise correlations are weak:

| Pair | Pearson correlation |
|---|---:|
| Price and views | -0.0571 |
| Price and rating | -0.0495 |
| Views and rating | +0.1334 |

In this sample, price alone has almost no linear relationship with views. These correlations are descriptive, not causal.

### View outliers

Using the 1.5×IQR rule on `total_views`, Q1 is 33, Q3 is 34, and the IQR is 1. The lower and upper fences are 31.5 and 35.5. This identifies **19 of 79 products (24.1%)** as statistical outliers:

| Outlier group | Count | Interpretation |
|---|---:|---|
| 0 views | 15 | No view events recorded in this extract |
| 2–3 views | 2 | Very low observed traffic |
| 2,803 views | 2 | High-traffic flagships: Apple iPhone 15 Pro Max and Samsung Galaxy S24 Ultra |

The view distribution is tightly clustered around 33–34 for most products, so the narrow IQR makes both very low and very high traffic statistical outliers. Zero recorded views should be checked against event coverage, join keys, and the reporting period before being interpreted as proof of no customer interest.

## 3. Strategic Portfolio Segmentation Matrix

The analysis applies two inclusive gates: **high traffic = at least 20 views** and **high rating = at least 4.2**. Products below either gate are assigned to the corresponding low quadrant.

| Segment | Rating and traffic criteria | Products | Share | Strategic response |
|---|---|---:|---:|---|
| **Stars** | Rating ≥ 4.2 and views ≥ 20 | 35 | 44.3% | Protect availability and listing quality; test cross-sell and upsell |
| **Hidden Gems** | Rating ≥ 4.2 and views < 20 | 17 | 21.5% | Validate tracking, then test search placement, content, and measured promotion |
| **At Risk** | Rating < 4.2 and views ≥ 20 | 27 | 34.2% | Audit product quality, customer feedback, and listing accuracy before expanding promotion |
| **Dead Weight** | Rating < 4.2 and views < 20 | 0 | 0.0% | No products fell in this quadrant in the current extract |

The segments sum to all 79 products. The absence of products in Dead Weight does not mean there are no low-performing products: 27 products have meaningful observed traffic but ratings below the 4.2 gate.

## 4. Database Integration & Review Audit

The Neon review extraction queried `catalog.dim_products`, `retail_traffic.fact_glance_views`, and `catalog.dim_reviews` using joins on ASIN. It selected products with at least 20 distinct view events and a product rating below 4.2, and exported **89 individual review rows** for the at-risk catalog.

### Extracted review ratings

| Individual review rating | Reviews |
|---:|---:|
| 1 star | 20 |
| 2 stars | 20 |
| 3 stars | 13 |
| 4 stars | 20 |
| 5 stars | 16 |
| **Total** | **89** |

The 1- and 2-star reviews together account for 40 of 89 extracted reviews (44.9%). The review export preview labels its review text as **synthetic demo reviews**. These counts are useful for validating the analysis workflow, but must not be represented as verified real-customer feedback.

The product-traffic refresh query in `eda/export_product_views.py` reached its CSV export step, but writing to `product_views_analysis.csv` failed with a `PermissionError`. The existing local traffic dataset was not overwritten. Accordingly, the portfolio counts and view analysis above describe the local 79-product CSV, while the review audit describes the Neon extract successfully written during this run. Confirm that both extracts use the same snapshot/reporting period before operational decisions.

## 5. Key Findings & Actionable Business Recommendations

### Priority products

| Product | Product-level rating | Views | Reviews in extract | Individual review evidence |
|---|---:|---:|---:|---|
| Studio Headphones Model 16 | 3.5 | 33 | 3 | All 3 extracted reviews are 1-star |
| Rice Cooker Model 32 | 3.5 | 34 | 4 | All 4 extracted reviews are 4-star |
| Machine Learning Handbook Model 48 | 3.5 | 33 | 3 | Average individual review rating is 2.0 |

Studio Headphones Model 16 is a clear quality-audit priority: it is At Risk and all three extracted individual reviews are 1-star. Rice Cooker Model 32 is also At Risk by its product-level rating and traffic, but the extracted reviews do **not** show a 1- or 2-star spike: all four are 4-star. The difference between its 3.5 product-level rating and the four extracted 4-star reviews warrants a rating-source, aggregation-window, or snapshot reconciliation—not a claim of negative feedback. Review counts are small, so validate against a larger time window before drawing conclusions.

### Recommended actions

1. **Audit the At-Risk catalog, starting with the lowest-rated products.** Review quality-control records, return/defect signals, product variants, and listing claims for Studio Headphones Model 16, Rice Cooker Model 32, and Machine Learning Handbook Model 48.
2. **Triage review evidence at the individual-review level.** For Studio Headphones Model 16, examine the three 1-star comments and map themes to product or fulfillment issues. For Rice Cooker Model 32, reconcile the catalog rating against its four 4-star extracted reviews before changing the listing or product.
3. **Fix measurement and listing coverage for the 15 zero-view products.** Check ASIN joins, event ingestion, reporting windows, listing status, and search discoverability. Treat zero as “no views recorded in this extract” until instrumentation is validated.
4. **Promote Hidden Gems through controlled experiments.** After traffic tracking is confirmed, run measured search-placement or content tests and evaluate incremental qualified views and conversion rather than assuming more exposure will convert.
5. **Protect Stars and avoid broad price-only interventions.** Maintain availability and accurate content for strong products. Because the observed price–views correlation is approximately zero, test merchandising and discoverability changes rather than relying on price cuts alone.
6. **Reconcile and refresh data before final investment decisions.** Resolve the permission issue preventing the product-traffic CSV refresh; align product, traffic, rating, and review extracts to one snapshot and reporting period.
7. **Treat review results as test data.** Replace or clearly segregate synthetic demo reviews before using review themes, counts, or sentiment in customer-facing or executive claims.

## Method and limitations

- Product segmentation and view-outlier counts are calculated from the 79-row local CSV.
- The IQR outlier test is applied to `total_views`; it is not an outlier test of ratings or prices.
- Correlation does not demonstrate causality.
- Review records are synthetic demo data, and per-product review samples are small.
- The Neon review extraction completed, but the separate refreshed product-traffic CSV could not be persisted because of a file-permission error.
