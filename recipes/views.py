from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from recipes.models import Recipe
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

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


#class RecipeDetailView()