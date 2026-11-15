from repositories.listings import ListingRepository


def predict_violation(item_id: int, repository: ListingRepository) -> bool:
    listing = repository.get(item_id)
    return not listing.is_verified_seller and listing.images_qty == 0
