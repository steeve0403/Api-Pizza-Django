from django.contrib.auth import authenticate
from django.conf import settings
import jwt
from ninja import Router

router = Router()

@router.post("/login/")
def login(request, username: str, password: str):
    user = authenticate(username=username, password=password)
    if user is None:
        token = jwt.encode({"username": user.username}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return {"token": token}
    return {"error": "Invalid credentials"}, 401