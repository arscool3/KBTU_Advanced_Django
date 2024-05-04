from rest_framework import routers

from . import views

r = routers.DefaultRouter()

r.register(r"students", views.StudentViewSet)

urlpatterns = r.urls
