from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from aiogram.types import Message

from tgbot.models.shop import SneakerBrand


async def add_sneaker_brand(brand_name: str, session: AsyncSession):
    sneaker_brand = SneakerBrand(name=brand_name) 
    session.add(sneaker_brand)
    try:
        await sneaker_brand.create()

        await session.commit()
        await session.refresh(user)
    except IntegrityError:
        await session.rollback()

    username = message.from_user.username if message.from_user.username else 'хз'
    
    user = User(tg_id=int(message.from_user.id), name=username)
    
    session.add(user)
    


async def edit_sneaker_brand():
    pass


async def detele_brand():
    pass


async def get_all_brands():
    pass


async def get_count_all_brands():
    pass


async def add_sneakers():
    pass


async def select_sneakers():
    pass


async def delete_sneakers():
    pass


async def get_all_sneakers_of_brand():
    pass


async def get_count_all_sneakers_of_brand():
    pass
