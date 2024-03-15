from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("v1/", include("rest_v2.urls")),
    path("v2/", include("rest_v1.urls")),
]
