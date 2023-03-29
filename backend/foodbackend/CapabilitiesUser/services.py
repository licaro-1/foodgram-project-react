from typing import Union

from django.shortcuts import get_object_or_404

from .models import Subscription, ShoppingCart, Favourites
from users.models import User
from Recipes.models import Recipe

"""Subscription Services"""

def delete_subscribtion_by_user_and_author(user: User, author: User)-> Union[None, False]:
    """Удаляет подписку пользователя на автора."""
    if not _user_is_author(user, author):
        subscribe = Subscription.objects.filter(
            user=user,
            author=author
        )
        if subscribe:
            subscribe.delete()
            return None
    return False


def create_subscribtion_by_user(user: User, author: User) -> Union[User, False]:
    """Создает подписку между пользователем и автором, если та отсутствует."""
    if not _check_already_subscribe(user, author) and not _user_is_author(user, author):
        subscribe = Subscription.objects.create(user=user, author=author)
        return subscribe
    return False


def _check_already_subscribe(user: User, author: User)-> bool:
    """Проверяет наличие подписки."""
    if Subscription.objects.filter(user=user, author=author).exists():
        return True
    return False


def _user_is_author(user, author) -> bool:
    """Проверяет, что передаваемый пользователь не является автором."""
    return user == author


"""ShoppingCart Services"""

def add_recipe_to_shopping_cart(author: User, recipe: Recipe) -> Union[Recipe, False]:
    """Добавляет рецепт в список покупок."""
    if not _check_recipe_in_shop_cart(author, recipe):
        ShoppingCart.objects.create(author=author, recipe=recipe)
        return recipe
    return False


def delete_recipe_from_shopping_cart(author: User, recipe: Recipe) -> Union[None, False]:
    """Удаляет рецепт из списка покупок."""
    if _check_recipe_in_shop_cart(author, recipe):
        ShoppingCart.objects.filter(author=author, recipe=recipe).delete()
        return None
    return False


def _check_recipe_in_shop_cart(author: User, recipe: Recipe) -> bool:
    """Проверяет, находится ли рецепт в списке покупок."""
    if ShoppingCart.objects.filter(author=author, recipe=recipe).exists():
        return True
    return False


"""Favourites Services"""

def add_recipe_to_favourite(author: User, recipe: Recipe) -> Union[None, False]:
    """Добавляет рецепт в список избранных."""
    if not _check_recipe_in_favourite(author, recipe):
        Favourites.objects.create(author=author, recipe=recipe)
        return None
    return False
    pass


def revome_recipe_from_favourite(author: User, recipe: Recipe) -> Union[None, False]:
    """Удаляет рецепт из списка избранных."""
    if _check_recipe_in_favourite(author, recipe):
        Favourites.objects.filter(author=author, recipe=recipe).delete()
        return None
    return False


def _check_recipe_in_favourite(author: User, recipe: Recipe) -> bool:
    """Проверяет, находится ли рецепт в списке избранных."""
    if Favourites.objects.filter(author=author, recipe=recipe).exists():
        return True
    return False