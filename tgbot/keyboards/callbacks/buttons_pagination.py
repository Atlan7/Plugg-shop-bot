from aiogram.filters.callback_data import CallbackData 


class ButtonsPaginationCallback(CallbackData, prefix="pg_cb"):
    action: str
    current_page: int
    total_pages: int
    buttons_action: str
    buttons_per_col: int = 8
    buttons_per_row: int = 1
