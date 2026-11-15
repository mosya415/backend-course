import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from repositories.listings import Listing, ListingRepository
from services import moderation

logger = logging.getLogger(__name__)
router = APIRouter()


class PredictRequest(BaseModel):
    model_config = ConfigDict(strict=True)

    seller_id: int
    is_verified_seller: bool
    item_id: int
    name: str
    description: str
    category: int
    images_qty: Annotated[int, Field(ge=0)]


@router.post(
    "/predict",
    response_model=bool,
    responses={
        400: {"description": "Некорректное тело запроса"},
        500: {"description": "Внутренняя ошибка сервиса"},
    },
)
async def predict(payload: PredictRequest) -> bool:
    repository = ListingRepository(Listing(**payload.model_dump()))
    try:
        return moderation.predict_violation(payload.item_id, repository)
    except Exception as exc:
        logger.exception("Moderation failed for listing %s", payload.item_id)
        raise HTTPException(status_code=500, detail="Internal server error") from exc
