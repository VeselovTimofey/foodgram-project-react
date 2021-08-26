from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from recipes.models import Ingredient, Purchase, Recipe, RecipeIngredient, Tag

from .forms import RecipeForm

User = get_user_model()


def get_ingredient(request):
    """ This function return ingredients which the user has chosen
     from create_recipe or update_recipe page. """
    ingredients = {}
    for key, value in request.POST.items():
        if key.startswith("nameIngredient"):
            number = key.split("_")[1]
            ingredients[value] = request.POST[f"valueIngredient_{number}"]
    return ingredients


def get_tag(request):
    """ This function return tags which the user has chosen
     from create_recipe or update_recipe page. """
    name_tag = {"breakfast": "Завтрак", "lunch": "Обед", "dinner": "Ужин"}
    tags = []
    for key, value in request.POST.items():
        if key in name_tag.keys():
            tags.append(name_tag[key])
    return tags


def get_old_ingredient(recipe):
    """ This function return old ingredients from database. """
    list_ingredient = []
    number_ingredient = 0
    for ingredient in recipe.ingredient.all():
        constituent_of_ingredient = []
        constituent_of_ingredient.append(ingredient.name)
        ingredient_count = list(recipe.ingredients_in_recipe.filter(
            ingredient=ingredient
        ).values_list("count"))
        constituent_of_ingredient.append(ingredient_count[0][0])
        constituent_of_ingredient.append(ingredient.unit)
        number_ingredient += 1
        constituent_of_ingredient.append(number_ingredient)
        list_ingredient.append(constituent_of_ingredient)
    return list_ingredient


def get_old_tag(recipe):
    """ This function return names of old tags from database. """
    list_tag = []
    for tag in Tag.objects.all():
        recipe_in_tag = list(tag.recipe_tag.all())
        if recipe in recipe_in_tag:
            list_tag.append(tag)
    return list_tag


def get_old_purchase(purchaser):
    """ This function return list with user purchase. """
    purchase = Purchase.objects.get_or_create(purchaser=purchaser)
    return purchase[0].purchases.all()


def get_old_favorite(user):
    """ This function return list with user favorite. """
    list_favorite = user.user_favorite.all()
    list_favorite_name = []
    for favorite in list_favorite:
        list_favorite_name.append(favorite.recipe)
    return list_favorite_name


def index(request):
    """ Main page that displays list of Recipes. """
    recipes = Recipe.objects.all()
    page_title = "Рецепты"
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        list_purchase = get_old_purchase(request.user)
        list_favorite_name = get_old_favorite(request.user)
        return render(request, "templates/index.html",
                      {"page_obj": page_obj,
                       "page_title": page_title,
                       "list_purchase": list_purchase,
                       "list_favorite_name": list_favorite_name})
    return render(request, "templates/index.html",
                  {"page_obj": page_obj, "page_title": page_title})


def tags_page(request, tag, author=None):
    """ This page display list of recipe, which has a current tag. """
    page_title = tag
    tags = ["Завтрак", "Обед", "Ужин"]
    if tag not in tags:
        return redirect(reverse("create_recipe"))
    if author:
        recipes = Recipe.objects.filter(
            author__username=author
        ).filter(tag__name=tag)
        html = "templates/profile.html"
    else:
        recipes = Recipe.objects.filter(tag__name=tag)
        html = "templates/index.html"
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        list_purchase = get_old_purchase(request.user)
        list_favorite_name = get_old_favorite(request.user)
        return render(request, html,
                      {"page_obj": page_obj,
                       "author": author,
                       "page_title": page_title,
                       "list_purchase": list_purchase,
                       "list_favorite_name": list_favorite_name})
    return render(request, html, {"page_obj": page_obj,
                                  "author": author,
                                  "page_title": page_title})


def recipe_detail(request, slug):
    """ Recipe page that displays components of recipe. """
    recipe = get_object_or_404(Recipe, slug=slug)
    list_ingredient = get_old_ingredient(recipe=recipe)
    list_tag = get_old_tag(recipe=recipe)
    page_title = recipe.name
    if request.user.is_authenticated:
        list_purchase = get_old_purchase(request.user)
        list_favorite_name = get_old_favorite(request.user)
        return render(request, "templates/recipe_detail.html",
                      {"recipe": recipe, "ingredients": list_ingredient,
                       "tags": list_tag, "page_title": page_title,
                       "list_purchase": list_purchase,
                       "list_favorite_name": list_favorite_name})
    return render(request, "templates/recipe_detail.html",
                  {"recipe": recipe, "ingredients": list_ingredient,
                   "tags": list_tag, "page_title": page_title})


@login_required
def favorite_page(request):
    """ Favorite page that displays list of favorite recipes. """
    page_title = "Избранное"
    recipes = Recipe.objects.filter(
        favorite_recipe__user__username=request.user
    )
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    list_purchase = get_old_purchase(request.user)
    list_favorite_name = get_old_favorite(request.user)
    return render(request, "templates/index.html",
                  {"page_obj": page_obj,
                   "page_title": page_title, "list_purchase": list_purchase,
                   "list_favorite_name": list_favorite_name})


def user_page(request, username):
    """ User page that display list of user recipes. """
    page_title = username
    recipes = Recipe.objects.filter(author__username=username)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        list_purchase = get_old_purchase(request.user)
        list_favorite_name = get_old_favorite(request.user)
        return render(request, "templates/profile.html",
                      {"page_obj": page_obj,
                       "author": username,
                       "page_title": page_title,
                       "list_purchase": list_purchase,
                       "list_favorite_name": list_favorite_name})
    return render(request, "templates/profile.html",
                  {"page_obj": page_obj, "author": username,
                   "page_title": page_title})


@login_required
def subscribe_page(request):
    """ List of current user`s Subscribe. """
    page_title = "Мои подписки"
    subscribe_list = []
    for user in User.objects.filter(
            subscriptions__who_subscribes__username=request.user
    ):
        constituent_of_subscripe = []
        constituent_of_subscripe.append(user)
        user_recipe = user.author_recipe.all()
        if user_recipe.count() > 3:
            constituent_of_subscripe.append(user_recipe[:3])
            constituent_of_subscripe.append(user_recipe.count() - 3)
        else:
            constituent_of_subscripe.append(user_recipe)
            constituent_of_subscripe.append(0)
        subscribe_list.append(constituent_of_subscripe)
    paginator = Paginator(subscribe_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    list_purchase = get_old_purchase(request.user)
    list_favorite_name = get_old_favorite(request.user)
    return render(request, "templates/my_subscribe.html",
                  {"page_obj": page_obj, "page_title": page_title,
                   "list_purchase": list_purchase,
                   "list_favorite_name": list_favorite_name})


@login_required
def purchase_page(request):
    """ List of current user`s Purchase """
    page_title = "Список покупок"
    recipes = Purchase.objects.get(purchaser=request.user).purchases.all()
    paginator = Paginator(recipes, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    list_purchase = get_old_purchase(request.user)
    list_favorite_name = get_old_favorite(request.user)
    return render(request, "templates/purchase.html",
                  {"page_obj": page_obj, "page_title": page_title,
                   "list_purchase": list_purchase,
                   "list_favorite_name": list_favorite_name})


@login_required
def create_recipe(request):
    """ This page create new recipe. """
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

    page_title = "Создать рецепт"
    list_purchase = get_old_purchase(request.user)
    list_favorite_name = get_old_favorite(request.user)

    if request.method != "POST":
        form = RecipeForm()
        return render(request, "templates/recipe_create.html",
                      {"form": form, "page_title": page_title,
                       "list_purchase": list_purchase,
                       "list_favorite_name": list_favorite_name})

    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.slug = create_slug(recipe.name)
        recipe.save()
        tags = get_tag(request)
        for name in tags:
            tag = get_object_or_404(Tag, name=name)
            recipe.tag.add(tag)
        ingredients = get_ingredient(request)
        for name in ingredients:
            ingredient = get_object_or_404(Ingredient, name=name)
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=ingredient,
                                            count=ingredients[name])
        return redirect(reverse("index"))

    return render(request, "templates/recipe_create.html",
                  {"form": form, "page_title": page_title,
                   "list_purchase": list_purchase,
                   "list_favorite_name": list_favorite_name})


@login_required
def update_recipe(request, slug):
    """ This page update recipe. """
    recipe = get_object_or_404(Recipe, slug=slug)
    page_title = f"Изменение рецепта {recipe.name}"
    list_purchase = get_old_purchase(request.user)
    list_favorite_name = get_old_favorite(request.user)
    tags = get_old_tag(recipe=recipe)
    list_tag = []
    for tag in tags:
        list_tag.append(tag.name)
    list_ingredient = get_old_ingredient(recipe=recipe)

    if request.user != recipe.author:
        return redirect(reverse("create_recipe"))

    form = RecipeForm(request.POST or None, instance=recipe)

    if request.method != "POST" or form.is_valid() is False:
        return render(request, "templates/recipe_update.html",
                      {"form": form, "recipe": recipe, "list_tag": list_tag,
                       "list_ingredient": list_ingredient,
                       "page_title": page_title,
                       "list_purchase": list_purchase,
                       "list_favorite_name": list_favorite_name})

    form.save()
    new_tags = get_tag(request)
    for tag in Tag.objects.all():
        if tag.name in new_tags and tag.name not in list_tag:
            recipe.tag.add(tag)
        elif tag.name not in new_tags and tag.name in list_tag:
            recipe.tag.remove(tag)
    ingredients = get_ingredient(request)
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    for name in ingredients:
        ingredient = get_object_or_404(Ingredient, name=name)
        RecipeIngredient.objects.create(recipe=recipe,
                                        ingredient=ingredient,
                                        count=ingredients[name])
    return redirect(reverse("recipe", kwargs={"slug": slug}))


def registration_request(request):
    """ If user tries to get to login_required page, he gets on this page. """
    page_title = "Необходима регистрация"
    return render(request, "templates/registration_request.html",
                  {"page_title": page_title})


def author_page(request):
    """ This page has information about the author. """
    page_title = "Об авторе"
    if request.user.is_authenticated:
        list_purchase = get_old_purchase(request.user)
        list_favorite_name = get_old_favorite(request.user)
        return render(request, "templates/author_page.html",
                      {"page_title": page_title,
                       "list_purchase": list_purchase,
                       "list_favorite_name": list_favorite_name})
    return render(request, "templates/author_page.html",
                  {"page_title": page_title})


def technology_page(request):
    """ This page has information about site technology. """
    page_title = "Технологии"
    if request.user.is_authenticated:
        list_purchase = get_old_purchase(request.user)
        list_favorite_name = get_old_favorite(request.user)
        return render(request, "templates/technology_page.html",
                      {"page_title": page_title,
                       "list_purchase": list_purchase,
                       "list_favorite_name": list_favorite_name})
    return render(request, "templates/technology_page.html",
                  {"page_title": page_title})


def page_not_found(request, exception):
    """ This page informs about the absence of a page. """
    page_title = "Страница не найдена"
    if request.user.is_authenticated:
        list_purchase = get_old_purchase(request.user)
        list_favorite_name = get_old_favorite(request.user)
        return render(request, "templates/404.html",
                      {"page_title": page_title,
                       "list_purchase": list_purchase,
                       "list_favorite_name": list_favorite_name,
                       "path": request.path}, status=404)
    return render(request, "templates/404.html",
                  {"page_title": page_title, "path": request.path}, status=404)


def server_error(request):
    """ This page informs about server error. """
    page_title = "Ошибка сервера"
    if request.user.is_authenticated:
        list_purchase = get_old_purchase(request.user)
        list_favorite_name = get_old_favorite(request.user)
        return render(request, "templates/500.html",
                      {"page_title": page_title,
                       "list_purchase": list_purchase,
                       "list_favorite_name": list_favorite_name}, status=500)
    return render(request, "templates/500.html",
                  {"page_title": page_title}, status=500)
