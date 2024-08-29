from django.urls import path
from ninja import NinjaAPI
from .views import router

api = NinjaAPI()
api.add_router("/api/", router)

urlpatterns = [
    path("", api.urls),
]
