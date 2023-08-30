from .start import start_message_router

from .help import help_message_router

from .cancel_process import cancel_process_router

from .add_new_brand import add_new_brand_router
from .view_brands import view_brands_router
from .edit_brand_name import edit_brand_name_router
from .delete_brand import delete_brand_router

from .add_new_sneakers import add_new_sneakers_router
from .view_sneakers_of_brand import view_sneakers_of_brand_router
from .edit_sneakers_name import edit_sneakers_name_router
from .edit_sneakers_price import edit_sneakers_price_router
from .edit_sneakers_photo import edit_sneakers_photo_router
from .delete_sneakers import delete_sneakers_router
from .change_user_start_message import change_user_start_message_router

admin_routers = [
    start_message_router,

    help_message_router,

    cancel_process_router,

    add_new_brand_router,
    view_brands_router,
    edit_brand_name_router,
    delete_brand_router,

    add_new_sneakers_router,
    view_sneakers_of_brand_router,
    edit_sneakers_name_router,
    edit_sneakers_price_router,
    edit_sneakers_photo_router,
    delete_sneakers_router,

    change_user_start_message_router
]


__all__ = [ 
    "admin_routers"
]
