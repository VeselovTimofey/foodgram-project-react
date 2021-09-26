from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from recipes.models import Purchase, Recipe
from recipes.utils import (authenticated_user_context_update,
                           get_recipe_ingredients, paginator_request,
                           tag_filter)

from .forms import RecipeForm

User = get_user_model()

TAGS = ["Завтрак", "Обед", "Ужин"]


def index(request):
    """ Main page that displays list of Recipes. """
    recipes = Recipe.objects.all()
    page_title = "Рецепты"
    page_obj = paginator_request(request, recipes)
    context = {"page_obj": page_obj, "page_title": page_title}
    context = authenticated_user_context_update(request, context)
    return render(request, "templates/index.html", context)


def tags_page(request, tag, author=None):
    """ This page display list of recipe, which has a current tag. """
    page_title = tag
    if tag not in TAGS:
        return redirect(reverse("index"))
    recipes, html = tag_filter(tag, author)
    page_obj = paginator_request(request, recipes)
    context = {
        "page_obj": page_obj, "author": author, "page_title": page_title
    }
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
    page_obj = paginator_request(request, recipes)
    context = {"page_obj": page_obj, "page_title": page_title}
    context = authenticated_user_context_update(request, context)
    return render(request, "templates/index.html", context)


def user_page(request, username):
    """ User page that display list of user recipes. """
    page_title = username
    recipes = Recipe.objects.filter(author__username=username)
    page_obj = paginator_request(request, recipes)
    context = {
        "page_obj": page_obj, "author": username, "page_title": page_title
    }
    context = authenticated_user_context_update(request, context)
    return render(request, "templates/profile.html", context)


@login_required
def subscribe_page(request):
    """ List of current user`s Subscribe. """
    page_title = "Мои подписки"
    subscribe_list = User.objects.filter(
            subscriptions__who_subscribes__username=request.user
    )
    page_obj = paginator_request(request, subscribe_list, 3)
    context = {"page_obj": page_obj, "page_title": page_title}
    context = authenticated_user_context_update(request, context)
    return render(request, "templates/my_subscribe.html", context)


@login_required
def purchase_page(request):
    """ List of current user`s Purchase """
    page_title = "Список покупок"
    purchase = get_object_or_404(Purchase, purchaser=request.user)
    recipes = purchase.purchases.all()
    if recipes.exists():
        page_obj = paginator_request(request, recipes, 3)
    else:
        page_obj = None
    context = {"page_obj": page_obj, "page_title": page_title}
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

    form = RecipeForm(request.POST or None, instance=recipe)

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
