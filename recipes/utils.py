from recipes.models import Ingredient, Purchase, Recipe
from django.conf import settings
from django.core.paginator import Paginator


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
    name_tag = {"breakfast": "Завтрак", "lunch": "Обед", "dinner": "Ужин"}
    tags = []
    for key, value in request.POST.items():
        if key in name_tag.keys():
            tags.append(name_tag[key])
    return tags


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
    list_favorites = user.favorites.all()
    list_favorites_name = []
    for favorite in list_favorites:
        list_favorites_name.append(favorite.recipe)
    return list_favorites_name


def authenticated_user_context_update(request, context):
    """ This function updates context with lists
     of user purchases and favorites. """
    if request.user.is_authenticated:
        list_purchases = get_user_purchases(request.user)
        list_favorites_name = get_user_favorites(request.user)
        context.update(list_purchases=list_purchases,
                       list_favorites_name=list_favorites_name)
    return context


def paginator_request(request, entity, number_of_pages=settings.NUMBER_OF_PAGES):
    """ This function get current page, object and number of pages.
     And return page_obj. """
    paginator = Paginator(entity, number_of_pages)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


def tag_filter(tag, author=None):
    """ This function filtered recipes by tag and, if necessary, author.
     And return filtered recipes and html. """
    if author:
        recipes = Recipe.objects.filter(
            author__username=author
        ).filter(tags__name=tag)
        html = "templates/profile.html"
    else:
        recipes = Recipe.objects.filter(tags__name=tag)
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
    for n in name:
        if n not in alphabet:
            continue
        slug += alphabet[n]
    return slug
