from typing import Union

from .models import Subscription, ShoppingCart, Favourites
from users.models import User
from recipes.models import Recipe

"""Subscription Services"""


def delete_subscribtion_by_user_and_author(user: User,
                                           author: User) -> Union[None, bool]:
    """Удаляет подписку пользователя на автора."""
    if not user == author:
        subscribe = Subscription.objects.filter(
            user=user,
            author=author
        )
        if subscribe:
            subscribe.delete()
            return None
    return False


def create_subscribtion_by_user(user: User,
                                author: User) -> Union[User, bool]:
    """Создает подписку между пользователем и автором, если та отсутствует."""
    if (not Subscription.objects.filter(user=user, author=author).exists()
            and not user == author):
        subscribe = Subscription.objects.create(user=user, author=author)
        return subscribe
    return False


"""ShoppingCart Services"""


def add_recipe_to_shopping_cart(author: User,
                                recipe: Recipe) -> Union[Recipe, bool]:
    """Добавляет рецепт в список покупок."""
    if not ShoppingCart.objects.filter(author=author, recipe=recipe).exists():
        ShoppingCart.objects.create(author=author, recipe=recipe)
        return recipe
    return False


def delete_recipe_from_shopping_cart(author: User,
                                     recipe: Recipe) -> Union[None, bool]:
    """Удаляет рецепт из списка покупок."""
    if ShoppingCart.objects.filter(author=author, recipe=recipe).exists():
        ShoppingCart.objects.filter(author=author, recipe=recipe).delete()
        return None
    return False


"""Favourites Services"""


def add_recipe_to_favourite(author: User,
                            recipe: Recipe) -> Union[None, bool]:
    """Добавляет рецепт в список избранных."""
    if not Favourites.objects.filter(author=author, recipe=recipe).exists():
        Favourites.objects.create(author=author, recipe=recipe)
        return None
    return False


def revome_recipe_from_favourite(author: User,
                                 recipe: Recipe) -> Union[None, bool]:
    """Удаляет рецепт из списка избранных."""
    if Favourites.objects.filter(author=author, recipe=recipe).exists():
        Favourites.objects.filter(author=author, recipe=recipe).delete()
        return None
    return False
