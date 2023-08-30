import logging

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from aiogram.types import Message

from tgbot.models.shop import Brand, Sneakers


#TODO: Rewrite this with two classes (class BrandModelOperations, class SneakersModelOprations)

async def add_to_db(item, session: AsyncSession):
    session.add(item)
    try:
        await session.commit()
        await session.refresh(item)
    except IntegrityError as err:
        await session.rollback()
        logging.error(err)


async def add_new_brand(brand_name: str, session: AsyncSession):
    sneaker_brand = Brand(name=brand_name) 
    await add_to_db(sneaker_brand, session)


async def get_brand_by_name(brand_name, session: AsyncSession) -> Brand:
    brand = await session.execute(select(Brand).where(Brand.name == brand_name))
    return brand.scalars().one_or_none()


async def get_all_brands(session: AsyncSession) -> List[Brand]:
    brands = await session.execute(select(Brand).order_by(Brand.id))
    return brands.scalars().all()


async def edit_brand_name(old_name: str, new_name: str, session: AsyncSession):
    brand = await get_brand_by_name(old_name, session) 
    brand.name = new_name 
    await session.flush()
    await session.commit()


async def delete_brand_by_name(brand_name: str, session: AsyncSession):
    brand = await get_brand_by_name(brand_name, session)
    try:
        await session.execute(delete(Sneakers).where(Sneakers.brand_id == brand.id))
        await session.execute(delete(Brand).where(Brand.id == brand.id))
        await session.commit()
    except Exception as err:
        await session.rollback()
        logging.error(err)


async def add_new_sneakers(brand_name: str, name: str, price: int, session: AsyncSession):
    brand = await get_brand_by_name(brand_name, session)
    sneakers = Sneakers(name=name, price=price, brand_id=brand.id, brand=brand) 
    await add_to_db(sneakers, session)


async def get_sneakers_by_id(sneakers_id: int, session: AsyncSession):
    sneakers = await session.execute(select(Sneakers).where(Sneakers.id == sneakers_id))
    return sneakers.scalars().one_or_none()


async def get_sneakers_by_name_and_brand(
        sneakers_name: str, 
        brand_name: str, 
        session: AsyncSession
    ):
    sneakers = await session.execute(
        select(Sneakers).where(
            Sneakers.name == sneakers_name and Sneakers.brand.name == brand_name
        )
    )
    return sneakers.scalars().one_or_none()


async def edit_sneakers_name(sneakers: Sneakers, new_name: str, session: AsyncSession):
    sneakers.name = new_name 
    await session.flush()
    await session.commit()


async def edit_sneakers_price(sneakers: Sneakers, new_price: int, session: AsyncSession):
    sneakers.price = new_price 
    await session.flush()
    await session.commit()


async def delete_sneakers_by_id(sneakers_id: int, session: AsyncSession):
    try:
        await session.execute(delete(Sneakers).where(Sneakers.id == sneakers_id))
        await session.commit()
    except Exception as err:
        await session.rollback()
        logging.error(err)


async def get_all_sneakers_of_brand(brand_name: str, session: AsyncSession):
    brand = await get_brand_by_name(brand_name, session)
    sneakers = await session.execute(select(Sneakers).where(Sneakers.brand_id == brand.id)) 
    sneakers = sneakers.scalars().all()
    return sneakers
