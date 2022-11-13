from fastapi import APIRouter, Depends

from core.dependencies import get_current_active_user
from core.schemas import User, ItemResponseCollectionBase, ItemBodySchema, SuccessResponseSchema, ItemUpdateSchema, \
    ItemInsertSchema
from db.db_ops import retrieve_items, update_single_item, delete_single_item, insert_new_item

router = APIRouter(
    prefix="/protected",
    tags=["items"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/items", tags=["items"], response_model=list[ItemResponseCollectionBase], status_code=200)
async def retrieve_item_list(limit: int, offset: int, current_user: User = Depends(get_current_active_user)):
    return await retrieve_items(limit=limit, offset=offset)


@router.get("/items/{item_id}", tags=["items"], response_model=ItemResponseCollectionBase, status_code=200)
async def fetch_item(item_id: str, current_user: User = Depends(get_current_active_user)):
    return await fetch_item(item_id=item_id)


@router.put("/items/{item_id}", tags=["items"], response_model=ItemResponseCollectionBase, status_code=200)
async def update_item(item_id: str, body: ItemBodySchema, current_user: User = Depends(get_current_active_user)):
    update_data = ItemUpdateSchema(
        item_id=item_id,
        entry_value=body.entry_value,
        is_active=body.is_active,
        rate=body.rate,
        carma=body.carma,
        user_id=current_user.id
    )
    return await update_single_item(data=update_data)


@router.delete("/items/{item_id}", tags=["items"], response_model=SuccessResponseSchema, status_code=200)
async def delete_item(item_id: str, current_user: User = Depends(get_current_active_user)):
    await delete_single_item(item_id=item_id)
    return {
        "success": True,
        "message": "Item was deleted successfully"
    }


@router.post("/items", tags=["items"], response_model=ItemResponseCollectionBase, status_code=201)
async def insert_item(body: ItemBodySchema, current_user: User = Depends(get_current_active_user)):
    item_insert_data = ItemInsertSchema(
        entry_value=body.entry_value,
        is_active=body.is_active,
        rate=body.rate,
        carma=body.carma,
        user_id=current_user.id
    )
    return await insert_new_item(data=item_insert_data)
