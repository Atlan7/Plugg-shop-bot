from .start import start_message_router

from .help import help_message_router

from .view_brands import view_brands_router
from .view_sneakers_of_brand import view_sneakers_of_brand_router

user_routers = [
    start_message_router,

    help_message_router,

    view_brands_router,
    view_sneakers_of_brand_router
]


__all__ = [ 
    "user_routers"
]
