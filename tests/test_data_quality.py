def is_valid_order(order: dict) -> bool:
    return (
        order.get("order_id") is not None
        and order.get("customer_id") is not None
        and order.get("order_date") is not None
        and order.get("order_total", -1) >= 0
    )


def test_valid_order_passes_quality_rules():
    order = {
        "order_id": "O1001",
        "customer_id": "C001",
        "order_date": "2026-05-01",
        "order_total": 120.50,
    }

    assert is_valid_order(order) is True


def test_invalid_order_fails_quality_rules():
    order = {
        "order_id": "O1003",
        "customer_id": None,
        "order_date": "2026-05-03",
        "order_total": -20.00,
    }

    assert is_valid_order(order) is False