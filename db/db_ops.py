from typing import Union

from core.database import database
from core.schemas import ItemInsertSchema, ItemUpdateSchema, ItemResponseCollectionBase, UserBase, \
    DestroyTokenInsertSchema, UserInsert


async def fetch_user_by_id(user_id: str) -> UserBase:
    query = """SELECT id, ext_id, display_name, user_name, is_active FROM users WHERE id = :user_id;"""
    values = {
        "user_id": user_id,
    }
    result = await database.execute(query=query, values=values)
    return result


async def fetch_user_by_ext_id(ext_id: str) -> UserBase:
    query = """SELECT id, ext_id, display_name, user_name, is_active FROM users WHERE ext_id = :ext_id limit 1;"""
    values = {
        "ext_id": ext_id,
    }
    result = await database.execute(query=query, values=values)
    return result


async def insert_user(data: UserInsert) -> str:
    query = """insert into users (ext_id, display_name, user_name, is_active)
                values (:ext_id, :display_name, :user_name, :is_active);"""
    values = {
        "ext_id": data.ext_id,
        "display_name": data.display_name,
        "user_name": data.user_name,
        "is_active": data.is_active
    }
    result = await database.execute(query=query, values=values)
    return result


async def make_token_dead(data: DestroyTokenInsertSchema) -> None:
    query = """insert into dead_tokens (ext_id, user_id, token_value)
                    values (:ext_id, :user_id, :token_value);"""
    values = {
        "ext_id": data.ext_id,
        "user_id": data.user_id,
        "token_value": data.token_value,
    }
    result = await database.execute(query=query, values=values)
    return result


async def retrieve_items(limit: int, offset: int) -> list[ItemResponseCollectionBase]:
    query = """SELECT * FROM items ORDER BY created_at DESC limit :limit_value offset :offet_value;"""
    values = {
        "limit_value": limit,
        "offset_value": offset
    }
    result = await database.execute(query=query, values=values)
    return result


async def fetch_item(item_id: str) -> Union[ItemResponseCollectionBase, None]:
    query = """SELECT * FROM items WHERE id = :item_id;"""
    values = {
        "item_id": item_id,
    }
    result = await database.execute(query=query, values=values)
    return result


async def delete_single_item(item_id: str) -> None:
    query = """DELETE FROM items WHERE id = :item_id;"""
    values = {
        "item_id": item_id,
    }
    await database.execute(query=query, values=values)


async def update_single_item(data: ItemUpdateSchema) -> ItemResponseCollectionBase:
    query = """update items set entry_value = :entry_value, is_active = :is_active, rate = :rate, carma = :carma, 
    user_id = :user_id where id = :item_id RETURNING *;"""
    values = {
        "entry_value": data.entry_value,
        "is_active": data.is_active,
        "rate": data.rate,
        "carma": data.carma,
        "user_id": data.user_id,
        "item_id": data.item_id
    }
    result = await database.execute(query=query, values=values)
    return result


async def insert_new_item(data: ItemInsertSchema) -> ItemResponseCollectionBase:
    query = """insert into items (entry_value, is_active, rate, carma, user_id)
                values (:entry_value, :is_active, :rate, :carma, :user_id) RETURNING *;"""
    values = {
        "entry_value": data.entry_value,
        "is_active": data.is_active,
        "rate": data.rate,
        "carma": data.carma,
        "user_id": data.user_id
    }
    result = await database.execute(query=query, values=values)
    return result
