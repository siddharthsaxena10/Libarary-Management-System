# FastAPI imports
from fastapi import APIRouter, Depends

# SQLAlchemy imports
from sqlalchemy.orm import Session

# Database connection
from app.db.database import get_db

# SQLAlchemy model
from app.models.shop import Shop as ShopModel

# Pydantic validation schema
from app.schemas.shop import ShopCreate


# Router create karo
router = APIRouter()


# POST API: shop ka data database mein save karegi
@router.post("/shops")
def create_shop(
    shop: ShopCreate,
    db: Session = Depends(get_db)
):
    # Request data se naya shop object banao
    new_shop = ShopModel(
        name=shop.name,
        address=shop.address,
        phone=shop.phone,
        price=shop.price
    )

    # Object ko database session mein add karo
    db.add(new_shop)

    # Database mein changes save karo
    db.commit()

    # Database se generated ID retrieve karo
    db.refresh(new_shop)

    # Response return karo
    return {
        "message": "Shop added successfully",
        "shop": {
            "shop_id": new_shop.shop_id,
            "name": new_shop.name,
            "address": new_shop.address,
            "phone": new_shop.phone,
            "price": float(new_shop.price)
        }
    }