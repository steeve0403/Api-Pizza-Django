from django.shortcuts import render
from ninja import Router
from .models import Pizza, Ingredient
from .schemas import PizzaSchema, IngredientSchema

# Create your views here.

router = Router()

@router.get("/pizzas", response=list[PizzaSchema])
def get_pizzas(request):
    return Pizza.objects.all()

# @router.get("/pizzas/{id}", response=list[PizzaSchema])
# def get_only_pizzas(request):
#     return Pizza.objects.get(pk=request.GET["id"])


@router.post("/pizzas", response=PizzaSchema)
def create_pizza(request, response: PizzaSchema):
    pizza_obj = Pizza.objects.create(**response.dict())
    return pizza_obj

@router.get("/ingredients", response=list[IngredientSchema])
def get_ingredients(request):
    return Ingredient.objects.all()