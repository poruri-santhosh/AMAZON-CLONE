import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()
import app

def run_tests():
    print("========================================")
    print("RUNNING AMAZON CLONE VERIFICATION TESTS")
    print("========================================")

    client = app.app.test_client()

    # 1. Test Storefront
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200 for /, got {res.status_code}"
    assert b"amazon" in res.data, "Amazon branding missing on /"
    print(" [PASS] 1. Storefront homepage rendered (200 OK)")

    # 2. Test Catalog Products API
    res = client.get("/api/products")
    assert res.status_code == 200
    data = res.get_json()
    assert data["count"] >= 19, f"Expected at least 19 products, got {data['count']}"
    print(f" [PASS] 2. Products API returned {data['count']} live products from Neon DB")

    # 3. Test Search & Filter
    res = client.get("/api/products?q=Sony")
    assert res.status_code == 200
    sony_data = res.get_json()
    assert sony_data["count"] >= 1, "Expected search for 'Sony' to return results"
    print(f" [PASS] 3. Search query 'Sony' returned {sony_data['count']} matching item(s)")

    # 4. Test Autocomplete Suggestions
    res = client.get("/api/search/suggestions?q=app")
    assert res.status_code == 200
    suggestions = res.get_json()
    assert len(suggestions) > 0, "Expected suggestions for 'app'"
    print(f" [PASS] 4. Search autocomplete suggestions returned {len(suggestions)} items")

    # 5. Test Product Detail & Reviews
    test_asin = "B09XS7JWHH" # Sony XM5
    res = client.get(f"/api/products/{test_asin}")
    assert res.status_code == 200
    pdp = res.get_json()
    assert pdp["asin"] == test_asin
    assert "reviews" in pdp and len(pdp["reviews"]) > 0
    print(f" [PASS] 5. Product Detail for {pdp['title']} returned with {len(pdp['reviews'])} customer reviews")

    # 6. Test Cart Add & View
    res = client.post("/api/cart/add", json={"asin": test_asin, "quantity": 2})
    assert res.status_code == 201
    add_data = res.get_json()
    print(f" [PASS] 6. Added 2 units of {test_asin} to cart (Cart total items: {add_data['cart_count']})")

    res = client.get("/api/cart")
    assert res.status_code == 200
    cart_data = res.get_json()
    assert len(cart_data["items"]) > 0
    print(f" [PASS] 7. Cart API verified: Subtotal = ${cart_data['subtotal']:.2f}")

    # 7. Test Wishlist Toggle
    res = client.post("/api/wishlist/toggle", json={"asin": test_asin})
    assert res.status_code == 200
    w_data = res.get_json()
    print(f" [PASS] 8. Wishlist toggle: in_wishlist={w_data['in_wishlist']}")

    # 8. Test Address Update
    res = client.post("/api/customer/address", json={"city": "San Francisco", "postal_code": "94105"})
    assert res.status_code == 200
    print(" [PASS] 9. Delivery destination updated to San Francisco 94105")

    # 9. Test Write Customer Review
    res = client.post(f"/api/products/{test_asin}/reviews", json={
        "rating": 5,
        "title": "Incredible sound isolation and all-day comfort!",
        "text": "Tested on cross-country flights and coffee shops. Best ANC in the market!"
    })
    assert res.status_code == 201
    rev_data = res.get_json()
    print(f" [PASS] 10. Customer review posted to Neon DB! New average rating: {rev_data['new_rating']}")

    # 10. Test Checkout
    res = client.post("/api/checkout", json={
        "shipping_name": "Alex Mercer",
        "shipping_address": "500 Howard St",
        "shipping_city": "San Francisco",
        "shipping_postal_code": "94105",
        "payment_method": "Amazon Pay (Balance $250.00)",
        "delivery_speed": "FREE Two-Day Shipping"
    })
    assert res.status_code == 201
    checkout_res = res.get_json()
    order_id = checkout_res["order_id"]
    print(f" [PASS] 11. Checkout transaction committed in Neon DB! Order ID: {order_id}, Total: ${checkout_res['total_amount']:.2f}")

    # 11. Test Orders List
    res = client.get("/api/orders")
    assert res.status_code == 200
    orders_data = res.get_json()
    assert orders_data["count"] > 0
    print(f" [PASS] 12. Order history queried: {orders_data['count']} orders found with real-time tracking timeline")

    # 12. Test Cancel Order
    res = client.post(f"/api/orders/{order_id}/cancel")
    assert res.status_code == 200
    cancel_data = res.get_json()
    print(f" [PASS] 13. Order cancellation verified: {cancel_data['message']}")

    print("========================================")
    print("ALL 13 MAJOR FUNCTIONALITY TESTS PASSED!")
    print("========================================")

if __name__ == "__main__":
    run_tests()
