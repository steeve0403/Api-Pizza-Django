from django.shortcuts import get_object_or_404
from ninja import Router
from django.db import transaction
from django.db.models import Q

from api.models.category import Category
from api.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from api.exception import BadRequestError

router = Router()


@router.get("/", response=list[CategorySchema])
def list_categories(request):
    categories = Category.objects.filter(is_deleted=False)
    return categories


@router.get("/{category_id}", response=CategorySchema)
def get_category(request, category_id: int):
    category = get_object_or_404(Category, id=category_id, is_deleted=False)
    return category


@router.post("/", response=CategorySchema)
@transaction.atomic
def create_category(request, data: CategoryCreateSchema):
    try:
        category = Category.objects.create(
            name=data.name,
            description=data.description,
            parent_id=data.parent_id,
            is_active=data.is_active
        )
        return category
    except Exception as e:
        raise BadRequestError(f"Failed to create category: {str(e)}")


@router.put("/{category_id}", response=CategorySchema)
@transaction.atomic
def update_category(request, category_id: int, data: CategoryUpdateSchema):
    category = get_object_or_404(Category, id=category_id, is_deleted=False)
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(category, attr, value)
    category.save()
    return category


@router.delete("/{category_id}")
def delete_category(request, category_id: int):
    category = get_object_or_404(Category, id=category_id, is_deleted=False)
    category.delete()  # Suppression logique
    return {"success": True}


@router.post("/{category_id}/restore/", response=CategorySchema)
def restore_category(request, category_id: int):
    category = get_object_or_404(Category, id=category_id, is_deleted=True)
    category.is_deleted = False
    category.save()
    return category


@router.get("/search/", response=list[CategorySchema])
def search_categories(request, query: str):
    categories = Category.objects.filter(
        (Q(name__icontains=query) | Q(description__icontains=query)) & Q(is_deleted=False)
    )
    return categories


@router.get("/{category_id}/children/", response=list[CategorySchema])
def list_subcategories(request, category_id: int):
    category = get_object_or_404(Category, id=category_id, is_deleted=False)
    subcategories = category.children.filter(is_deleted=False)
    return subcategories
