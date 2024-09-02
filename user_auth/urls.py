from django.urls import path
from .auth_user import auth_user

urlpatterns = [
    path('', auth_user.urls),

]
