from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.list import ListView
from recipes.models import Recipe, RecipeIngredient, Ingredient, Tag
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RecipeForm

User = get_user_model()


class BaseRecipeListView(ListView):
    """ Base view for Recipes list. """
    context_object_name = "recipe_list"
    queryset = Recipe.objects.all()
    paginate_by = 6
    page_title = None

    def get_context_data(self, **kwargs):
        kwargs.update({"page_title": self._get_page_title()})
        return super().get_context_data(**kwargs)

    def _get_page_title(self):
        assert self.page_title, f"Attribute 'page_title' not set for {self.__class__.__name__}"
        return self.page_title


class IndexView(BaseRecipeListView):
    """ Main page that displays list of Recipes. """
    page_title = "Recipes"
    template_name = "templates/index.html"


class FavoriteView(LoginRequiredMixin, BaseRecipeListView):
    """ List of current user`s favorite Recipes. """
    page_title = "Recipes"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(favorites_user=self.request.user)
        return qs


class ProfileView(BaseRecipeListView):
    """ User`s page with its name and list of authored Recipes. """
    template_name = "templates/profile.html"

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs.get("username"))
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.user)
        return qs

    def _get_page_title(self):
        return self.user.get_full_name()


class RecipeDetailView(DetailView):
    """Page with Recipe details."""
    queryset = Recipe.objects.all()
    template_name = "templates/recipe_detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        #qs = qs.with_is_favorite(user_id=self.request.user.id)
        return qs


def create_recipe(request):

    def create_slug(name):
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
            if n in ["ь", "ъ", " "]:
                continue
            slug += alphabet[n]
        return slug

    def get_ingredient():
        ingredients = {}
        for key, value in request.POST.items():
            if key.startswith("nameIngredient"):
                number = key.split("_")[1]
                ingredients[value] = request.POST[f"valueIngredient_{number}"]
        return ingredients

    def get_tag():
        name_tag = {"breakfast": "Завтрак", "lunch": "Обед", "dinner": "Ужин"}
        tags = []
        for key, value in request.POST.items():
            if key in name_tag.keys():
                tags.append(name_tag[key])
        return tags

    if request.method != "POST":
        form = RecipeForm()

        return render(request, "templates/recipe_create.html", {"form": form})

    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.slug = create_slug(recipe.name)
        recipe.save()
        tags = get_tag()
        for name in tags:
            tag = get_object_or_404(Tag, name=name)
            recipe.tag.add(tag)
        ingredients = get_ingredient()
        for name in ingredients:
            ingredient = get_object_or_404(Ingredient, name=name)
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=ingredient,
                                            count=ingredients[name])
        return redirect(reverse("index"))

    return render(request, "templates/recipe_create.html", {"form": form})
