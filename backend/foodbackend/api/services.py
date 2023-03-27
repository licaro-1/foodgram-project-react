import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from Recipes.models import Recipe, RecipeTags, RecipeIngredients

class ImageField(serializers.ImageField):
    """Поле для изображения."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IsFavAndInShopCart(serializers.Serializer):
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    def get_is_in_shopping_cart(self, obj):
        """Проверка на вхождение рецепта в список покупок."""
        request = self.context['request']
        if request.user.is_authenticated:
            recipe = Recipe.objects.get(id=obj.id)
            recipe_in_shop_cart = recipe.recipes_shop_cart.filter(
                author=request.user
            )
            if recipe_in_shop_cart:
                return True
        return False

    def get_is_favorited(self, obj):
        """Проверка на вхождение рецепта в список избранных."""
        request = self.context['request']
        if request.user.is_authenticated:
            recipe = Recipe.objects.get(id=obj.id)
            recipe_is_favorited = recipe.recipes_fav.filter(
                author=request.user
            )
            if len(recipe_is_favorited) != 0:
                return True
        return False

def create_update_recipe_tags_ingredients(recipe, tags_list = None, ingredients_list = None):
    """Обновляет или создает теги и ингредиенты для рецепта."""
    if tags_list:
        recipe.tags.clear()
        for tag in tags_list:
            recipe.tags.add(tag)
            recipe.save()
    if ingredients_list:
        RecipeIngredients.objects.filter(recipe=recipe).delete()
        for ingredient in ingredients_list:
            if not RecipeIngredients.objects.filter(
                ingredient_id=ingredient['ingredient']['id'],
                recipe=recipe
            ).exists():
                recipeingredient = RecipeIngredients.objects.create(
                    ingredient_id=ingredient['ingredient']['id'],
                    recipe=recipe,
                    amount=ingredient['amount']
                )
                recipeingredient.save()
    return recipe
