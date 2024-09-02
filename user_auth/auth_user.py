from ninja import NinjaAPI

from user_auth.security import JWTAuth
from .views import register as register_router, login as login_router, logout as logout_router, \
    token_refresh as token_refresh, create_api_key as create_api_key, list_api_keys as list_api_keys, \
    revoke_api_key as revoke_api_key, list_sessions as list_sessions, revoke_session as revoke_session

auth_user = NinjaAPI(
    # auth=JWTAuth(),
    title="Auth User API",
    version="1.0.0",
    description="API pour gérer l'authentification et les utilisateurs",
)


auth_user.add_router("/register/", register_router, tags=["register"])
auth_user.add_router("/login/", login_router, tags=["login"])
auth_user.add_router("/logout/", logout_router, tags=["logout"])
auth_user.add_router("/token/", token_refresh, tags=["token"])
auth_user.add_router("/api-keys/", create_api_key, tags=["api_key"])
auth_user.add_router("/api-keys/", token_refresh, tags=["token_refresh"])
auth_user.add_router("/api-keys/", revoke_api_key, tags=["revoke"])
auth_user.add_router("/sessions/", list_sessions, tags=["sessions"])
auth_user.add_router("/sessions/", revoke_session, tags=["revoke"])


# Gestionnaire global d'exceptions
# @auth_user.exception_handler(Exception)
# def global_exception_handler(request, exc):
#     return auth_user.create_response(request, {"detail": "Une erreur s'est produite : " + str(exc)}, status=500)
