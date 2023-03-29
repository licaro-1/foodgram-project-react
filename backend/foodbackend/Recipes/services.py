from .models import RecipeIngredients


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


def _get_ingredients_dictionary_by_user(user):
    """
    Возвращает словарь ингредиентов из рецептов
    находящихся в списке покупок пользователя.
    """
    shop_cart_list = {}
    for ingredient_name, measanumerate, amount in RecipeIngredients.objects.filter(
        recipe__recipes_shop_cart__author=user
        ).values_list('ingredient__name', 'ingredient__measurement_unit', 'amount'):
        title = f'{ingredient_name} ({measanumerate})'
        if title not in shop_cart_list.keys():
            shop_cart_list[title] = int(amount)
        else:
            shop_cart_list[title] += int(amount)
    return shop_cart_list
