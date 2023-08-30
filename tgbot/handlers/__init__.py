"""Import all routers and add them to routers_list."""
from .admins.admin_handler import admin_routers
from .users.user_handler import user_routers

routers_list = [
    *user_routers,
    *admin_routers,
]

__all__ = [
    "routers_list",
]
