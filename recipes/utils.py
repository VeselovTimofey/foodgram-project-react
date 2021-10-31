from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from recipes.models import Ingredient, Purchase, Recipe, Tag

User = get_user_model()


def get_selected_ingredients(request):
    """ This function return ingredients which the user has chosen
     from create_recipe or update_recipe page. """
    ingredients = {}
    for key, value in request.POST.items():
        if key.startswith("nameIngredient"):
            number = key.split("_")[1]
            ingredients[value] = request.POST[f"valueIngredient_{number}"]
    return ingredients


def get_selected_tags(request):
    """ This function return tags which the user has chosen
     from create_recipe or update_recipe page. """
    tags = Tag.objects.all().values_list("name", flat=True)
    list_tags = []
    for key, value in request.POST.items():
        if key in tags:
            list_tags.append(key)
    return list_tags


def checking_ingredients_for_errors(request, form):
    """This function checking ingredients for uniqueness
     and positiveness of their value"""
    ingredients = []
    for key, value in request.POST.items():
        if key.startswith("nameIngredient"):
            if value in ingredients:
                form.add_error(None, "Ингредиенты должны быть уникальны.")
            number = key.split("_")[1]
            ingredient_count = int(request.POST[f"valueIngredient_{number}"])
            if ingredient_count <= 0:
                form.add_error(None, f"Кол-во {value} должно быть больше 0.")
            ingredients.append(value)


def get_recipe_ingredients(recipe):
    """ This function return old ingredients from database. """
    list_ingredients = Ingredient.objects.filter(
        recipe=recipe
    ).values_list("name", "ingredient_in_recipes__count", "unit", "id")
    return list_ingredients


def get_user_purchases(purchaser):
    """ This function return list with user purchase. """
    purchases = Purchase.objects.get_or_create(purchaser=purchaser)
    return purchases[0].purchases.all()


def get_user_favorites(user):
    """ This function return list with user favorite. """
    favorites = user.favorites.all()
    list_favorites_name = Recipe.objects.filter(favorites__in=favorites)
    return list_favorites_name


def tags_context_update(context):
    """ This function updates context with tags. """
    tags = Tag.objects.all()
    context.update(tags=tags)
    if "old_tags" not in context:
        context.update(old_tags=[])
    return context


def authenticated_user_context_update(request, context):
    """ This function updates context with lists
     of user purchases and favorites. """
    if request.user.is_authenticated:
        list_purchases = get_user_purchases(request.user)
        list_favorites_name = get_user_favorites(request.user)
        context.update(list_purchases=list_purchases,
                       list_favorites_name=list_favorites_name)
    return context


def paginator_request(request, entity,
                      number_of_pages=settings.NUMBER_OF_PAGES):
    """ This function get current page, object and number of pages.
     And return context with page_obj, page_range and paginator. """
    paginator = Paginator(entity, number_of_pages)
    page_number = request.GET.get("page")
    page_range = paginator.get_elided_page_range(
        number=page_number if page_number else 1, on_each_side=1, on_ends=0
    )
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "page_range": list(page_range)}
    return context


def tag_filter(tags, author=None, favorite_user=None):
    """ This function filtered recipes by tag and, if necessary, author.
     And return filtered recipes and html. """
    if author:
        recipes = Recipe.objects.filter(
            author__username=author
        ).filter(tags__name__in=tags).distinct()
        html = "templates/profile.html"
    elif favorite_user:
        recipes = Recipe.objects.filter(
            favorites__user__username=favorite_user
        ).filter(tags__name__in=tags).distinct()
        html = "templates/index.html"
    else:
        recipes = Recipe.objects.filter(tags__name__in=tags).distinct()
        html = "templates/index.html"
    return recipes, html


def create_slug(name):
    """ This function return transcription names in Latin letters. """
    name = name.lower()
    alphabet = {"а": "a", "б": "b", "в": "f", "г": "g", "д": "d",
                "е": "e", "ё": "e", "ж": "sh", "з": "z", "и": "i",
                "й": "i", "к": "k", "л": "l", "м": "m", "н": "n",
                "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
                "у": "u", "ф": "v", "х": "h", "ц": "c", "ч": "ch",
                "ш": "sh", "щ": "sh", "ы": "i", "э": "e", "ю": "ai",
                "я": "yi"}
    slug = ""
    for letter in name:
        if letter not in alphabet:
            continue
        slug += alphabet[letter]
    return slug


def create_subscribe_list(request):
    """ This function create subscribe list """
    subscribe_list = User.objects.filter(
        subscriptions__who_subscribes__username=request.user
    )
    return subscribe_list
