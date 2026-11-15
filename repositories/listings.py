from dataclasses import dataclass


@dataclass(frozen=True)
class Listing:
    item_id: int
    seller_id: int
    is_verified_seller: bool
    name: str
    description: str
    category: int
    images_qty: int


class ListingRepository:
    """In-memory snapshot of the listing supplied by the current request."""

    def __init__(self, listing: Listing) -> None:
        self._listing = listing

    def get(self, item_id: int) -> Listing:
        if self._listing.item_id != item_id:
            raise LookupError(f"Listing {item_id} was not found")
        return self._listing
