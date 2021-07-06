from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("active_listings", views.show_listings, name="active_listings"),
    path("create_listings", views.create_listing, name="create_listings"),
    re_path(r"listings/(?P<site>[\w]+)$", views.show_one_listing, name = "listing")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
