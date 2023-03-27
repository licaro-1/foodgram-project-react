from django_filters import rest_framework as filters

from Recipes.models import Recipe, Ingredient
from users.models import User


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author_id')
    tags = filters.CharFilter(field_name='tags__slug', lookup_expr='icontains')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value==1:
            return queryset.filter(
                recipes_fav__author=self.request.user
            ).all()
        return queryset.all().exclude(recipes_fav__author=self.request.user)
    
    def filter_is_in_shopping_cart(self,queryset, name, value):
        if self.request.user.is_authenticated:
            return queryset.filter(
                recipes_shop_cart__author=self.request.user
            )
        return queryset.all().exclude(
            recipes_shop_cart__author=self.request.user
        )

class IngredientFilter(filters.FilterSet):

    class Meta:
        model = Ingredient
        fields = ('name',)