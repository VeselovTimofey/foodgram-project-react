from django_filters import FilterSet

from recipes.models import Ingredient


class IngredientFilter(FilterSet):
    class Meta:
        model = Ingredient
        fields = ["name", ]

    @property
    def qs(self):
        queryset = super().qs
        name = self.request.query_params.get("query", None)
        if name:
            name = name[:-1]
        return queryset.filter(name=name)
