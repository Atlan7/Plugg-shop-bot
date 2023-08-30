import os 
import shutil

from typing import Dict

from aiogram import Bot
from aiogram.types import Message, InputMediaPhoto

from tgbot.config import preloaded_config

base_media_path = preloaded_config.media.base_path


async def download_sneakers_photo(
        photo: InputMediaPhoto, 
        bot: Bot, 
        data: Dict, 
        new_photo=True
    ): 
    photo_path = f'{base_media_path}/{data["brand_name"]}/{data["sneakers_name"]}.jpg' 
    os.makedirs(os.path.dirname(photo_path), exist_ok=True)
    await bot.download(photo, destination=photo_path)

def delete_sneakers_photo(brand_name: str, sneakers_name: str):
    photo_path = f'{base_media_path}/{brand_name}/{sneakers_name}.jpg' 
    if os.path.exists(photo_path):
        os.remove(photo_path)


def delete_brand_images(brand_name: str):
    shutil.rmtree(f'{base_media_path}/{brand_name}', ignore_errors=True)


def rename_img_dir_for_brand(old_brand_name: str, new_brand_name: str):
    old_path = f'{base_media_path}/{old_brand_name}'
    if os.path.exists(old_path):
        new_path = f'{base_media_path}/{new_brand_name}'
        os.rename(old_path, new_path)


def rename_sneakers_img(sneakers_brand: str, old_sneakers_name: str, new_sneakers_name: str):
    img_dir_path = f'{base_media_path}/{sneakers_brand}'
    old_path = f'{img_dir_path}/{old_sneakers_name}.jpg'
    if os.path.exists(old_path):
        new_path = f'{img_dir_path}/{new_sneakers_name}.jpg' 
        os.rename(old_path, new_path)
