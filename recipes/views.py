from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from recipes.models import Purchase, Recipe
from recipes.utils import (authenticated_user_context_update,
                           checking_ingredients_for_errors,
                           create_subscribe_list, get_recipe_ingredients,
                           paginator_request, tag_filter, tags_context_update)

from .forms import RecipeForm

User = get_user_model()

TAGS = ["Завтрак", "Обед", "Ужин"]


def index(request):
    """ Main page that displays list of Recipes. """
    recipes = Recipe.objects.all()
    page_title = "Рецепты"
    context = paginator_request(request, recipes)
    context.update(page_title=page_title)
    context = tags_context_update(context)
    context = authenticated_user_context_update(request, context)
    return render(request, "templates/index.html", context)


def tags_page(request, tags, author=None, favorite_user=None):
    """ This page display list of recipe, which has a current tags. """
    if tags == "Нет тегов" and author:
        return redirect(reverse("profile", kwargs={"username": author}))
    elif tags == "Нет тегов" and favorite_user:
        return redirect(reverse("favorite"))
    elif tags == "Нет тегов":
        return redirect(reverse("index"))
    if author:
        page_title = author
    elif favorite_user:
        page_title = "Избранное"
    else:
        page_title = "Рецепты"
    old_tags = tags.split()
    recipes, html = tag_filter(old_tags, author, favorite_user)
    context = paginator_request(request, recipes)
    if author:
        author = get_object_or_404(User, username=author)
        subscribe = create_subscribe_list(request)
        context.update(subscribe=subscribe)
    context.update(page_title=page_title, author=author,
                   favorite_user=favorite_user, old_tags=old_tags)
    context = tags_context_update(context)
    context = authenticated_user_context_update(request, context)
    return render(request, html, context)


def recipe_detail(request, slug):
    """ Recipe page that displays components of recipe. """
    recipe = get_object_or_404(Recipe, slug=slug)
    list_ingredient = get_recipe_ingredients(recipe=recipe)
    page_title = recipe.name
    context = {"recipe": recipe, "ingredients": list_ingredient,
               "page_title": page_title}
    context = authenticated_user_context_update(request, context)
    if request.user.is_authenticated:
        subscribe = request.user.who_subscribes.all().values_list(
            "who_are_subscribed_to", flat=True
        )
        context.update(subscribe=subscribe)
    return render(request, "templates/recipe_detail.html", context)


@login_required
def favorite_page(request):
    """ Favorite page that displays list of favorite recipes. """
    page_title = "Избранное"
    recipes = Recipe.objects.filter(
        favorites__user__username=request.user
    )
    context = paginator_request(request, recipes)
    context.update(page_title=page_title, favorite_user=request.user)
    context = tags_context_update(context)
    context = authenticated_user_context_update(request, context)
    return render(request, "templates/index.html", context)


def user_page(request, username):
    """ User page that display list of user recipes. """
    page_title = username
    recipes = Recipe.objects.filter(author__username=username)
    author = get_object_or_404(User, username=username)
    context = paginator_request(request, recipes)
    context.update(author=author, page_title=page_title)
    context = tags_context_update(context)
    context = authenticated_user_context_update(request, context)
    if request.user.is_authenticated:
        subscribe = create_subscribe_list(request)
        context.update(subscribe=subscribe)
    return render(request, "templates/profile.html", context)


@login_required
def subscribe_page(request):
    """ List of current user`s Subscribe. """
    page_title = "Мои подписки"
    subscribe_list = create_subscribe_list(request)
    context = paginator_request(request, subscribe_list, 3)
    context.update(page_title=page_title)
    context = authenticated_user_context_update(request, context)
    return render(request, "templates/my_subscribe.html", context)


@login_required
def purchase_page(request):
    """ List of current user`s Purchase """
    page_title = "Список покупок"
    purchase = get_object_or_404(Purchase, purchaser=request.user)
    recipes = purchase.purchases.all()
    if recipes.exists():
        context = paginator_request(request, recipes, 3)
    else:
        context = {}
    context.update(page_title=page_title)
    context = authenticated_user_context_update(request, context)
    return render(request, "templates/purchase.html", context)


@login_required
def create_recipe(request):
    """ This page create new recipe. """
    page_title = "Создать рецепт"
    context = authenticated_user_context_update(
        request, context={"page_title": page_title}
    )

    if request.method != "POST":
        form = RecipeForm()
        context.update(form=form)
        return render(request, "templates/recipe_create.html", context)

    form = RecipeForm(request.POST or None, files=request.FILES or None)
    context.update(form=form)
    checking_ingredients_for_errors(request, form)

    if form.is_valid():
        form.save(request)
        return redirect(reverse("index"))

    return render(request, "templates/recipe_create.html", context)


@login_required
def update_recipe(request, slug):
    """ This page update recipe. """
    recipe = get_object_or_404(Recipe, slug=slug)
    page_title = f"Изменение рецепта {recipe.name}"
    list_tag = recipe.tags.all().values_list("name", flat=True)
    list_ingredient = get_recipe_ingredients(recipe=recipe)

    if request.user != recipe.author:
        return redirect(reverse("create_recipe"))

    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )
    checking_ingredients_for_errors(request, form)

    context = {"form": form, "recipe": recipe, "list_tag": list_tag,
               "list_ingredient": list_ingredient, "page_title": page_title}
    context = authenticated_user_context_update(request, context)

    if request.method != "POST" or not form.is_valid():
        return render(request, "templates/recipe_create.html", context)

    form.save(request)
    return redirect(reverse("index"))


@login_required
def delete_recipe(request, slug):
    """ This function delete recipe and redirect to main page. """
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.user == recipe.author:
        recipe.delete()
    return redirect(reverse("index"))


def registration_request(request):
    """ If user tries to get to login_required page, he gets on this page. """
    page_title = "Необходима регистрация"
    return render(request, "templates/registration_request.html",
                  {"page_title": page_title})


def author_page(request):
    """ This page has information about the author. """
    page_title = "Об авторе"
    context = authenticated_user_context_update(
        request, context={"page_title": page_title}
    )
    return render(request, "templates/author_page.html", context)


def technology_page(request):
    """ This page has information about site technology. """
    page_title = "Технологии"
    context = authenticated_user_context_update(
        request, context={"page_title": page_title}
    )
    return render(request, "templates/technology_page.html", context)
