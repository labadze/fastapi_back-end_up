from fastapi import APIRouter, Depends

from core.dependencies import get_current_active_user
from core.schemas import User, DestroyTokenBodySchema, SuccessResponseSchema, DestroyTokenInsertSchema
from core.utils import decode_base64_string
from db.db_ops import make_token_dead

router = APIRouter(
    prefix="/private",
    tags=["account"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/account", tags=["account"], response_model=User, status_code=200)
async def get_current_user(current_user: User = Depends(get_current_active_user)):
    print(current_user)
    return current_user


@router.patch("/account/destroy_token/{user_id}", tags=["account"],
              response_model=SuccessResponseSchema, status_code=200)
async def destroy_token(user_id: str, body: DestroyTokenBodySchema,
                        current_user: User = Depends(get_current_active_user)):
    dead_token_data = DestroyTokenInsertSchema(
        ext_id=current_user.ext_id,
        user_id=await decode_base64_string(user_id),
        token_value=body.access_token
    )
    await make_token_dead(data=dead_token_data)
    return {
        "success": True,
        "message": "Session terminated, operation success."
    }
