from django.urls import path
from ninja import NinjaAPI
from .views import router


app_name = 'api'
api = NinjaAPI()
api.add_router("/", router)


