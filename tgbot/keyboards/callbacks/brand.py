from aiogram.filters.callback_data import CallbackData 


class BrandCallback(CallbackData, prefix="brand_callback"):
    action: str
    brand: str
