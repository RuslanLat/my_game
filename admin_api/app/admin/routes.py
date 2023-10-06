# admin_api/app/admin/routes.py

import typing

from app.admin.views import AdminCurrentView

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:

    """Функция установки routes для работы
    с админом

    Args:
        app (Application): _description_
    """
    
    from app.admin.views import AdminLoginView, AdminAddView

    app.router.add_view("/admin.login", AdminLoginView)
    app.router.add_view("/admin.current", AdminCurrentView)
    app.router.add_view("/admin.add", AdminAddView)
