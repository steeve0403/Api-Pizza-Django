from ninja import NinjaAPI

from .jwt_auth import JWTAuth
from .views.pizza import router as pizza_router
from .views.ingredients import router as ingredient_router
from .views.image import router as image_router
from .views.category import router as category_router

# Configuration de l'API
api = NinjaAPI(
    title="Pizza API",
    version="1.0.0",
    description="API pour gérer les pizzas, les ingrédients et les catégories.",
    # docs_url="/api/docs",  # URL de la documentation interactive
    openapi_url="/openapi.json"  # URL de la documentation OpenAPI)
)
"""
    title="Pizza API",
    version="1.0.0",
    description="API pour gérer les pizzas, les ingrédients et les catégories.",
    docs_url="/api/docs",  # URL de la documentation interactive
    openapi_url="/api/openapi.json"  # URL de la documentation OpenAPI
    """

api.add_router("/pizzas/", pizza_router, tags=["Pizzas"])
api.add_router("/ingredients/", ingredient_router, tags=["Ingrédients"])
api.add_router("/categories/", category_router, tags=["Catégories"])
api.add_router("/images/", image_router, tags=["Images"])


# Gestionnaire global d'exceptions
@api.exception_handler(Exception)
def global_exception_handler(request, exc):
    return api.create_response(request, {"detail": "Une erreur s'est produite : " + str(exc)}, status=500)
