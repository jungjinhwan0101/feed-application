from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from api.account.views import UserViewSet

router = SimpleRouter(trailing_slash=False)
router.register("api/users", UserViewSet, basename="users")


urlpatterns = [
    path("admin/", admin.site.urls),
]
urlpatterns += router.urls
