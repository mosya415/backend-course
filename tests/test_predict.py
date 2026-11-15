import pytest
from fastapi.testclient import TestClient

from main import app
from repositories.listings import Listing, ListingRepository
from services import moderation


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def listing_data():
    return {
        "seller_id": 13,
        "is_verified_seller": False,
        "item_id": 42,
        "name": "Стол",
        "description": "Деревянный стол",
        "category": 2,
        "images_qty": 0,
    }


@pytest.mark.parametrize(
    ("verified", "image_count", "expected"),
    [(True, 0, False), (True, 2, False), (False, 1, False), (False, 0, True)],
)
def test_predict(client, listing_data, verified, image_count, expected):
    listing_data.update(is_verified_seller=verified, images_qty=image_count)

    response = client.post("/predict", json=listing_data)

    assert response.status_code == 200
    assert response.json() is expected


@pytest.mark.parametrize(
    "field",
    ["seller_id", "is_verified_seller", "item_id", "name", "description", "category", "images_qty"],
)
def test_required_fields(client, listing_data, field):
    del listing_data[field]

    response = client.post("/predict", json=listing_data)

    assert response.status_code == 400
    assert response.json()["detail"][0]["loc"] == ["body", field]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("seller_id", "13"),
        ("is_verified_seller", "false"),
        ("item_id", True),
        ("name", 12),
        ("description", None),
        ("category", 2.5),
        ("images_qty", -1),
        ("images_qty", "2"),
    ],
)
def test_invalid_fields(client, listing_data, field, value):
    listing_data[field] = value

    response = client.post("/predict", json=listing_data)

    assert response.status_code == 400
    assert response.json()["detail"][0]["loc"] == ["body", field]


def test_malformed_json(client):
    response = client.post("/predict", content=b"{", headers={"Content-Type": "application/json"})

    assert response.status_code == 400
    assert response.json()["detail"][0]["type"] == "json_invalid"


def test_business_logic_error(client, listing_data, monkeypatch):
    def failing_prediction(*args):
        raise RuntimeError("Test failure inside service")

    monkeypatch.setattr(moderation, "predict_violation", failing_prediction)

    response = client.post("/predict", json=listing_data)

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}


def test_service_predicts_violation_without_http(listing_data):
    listing = Listing(**listing_data)
    repository = ListingRepository(listing)

    assert moderation.predict_violation(listing.item_id, repository) is True
