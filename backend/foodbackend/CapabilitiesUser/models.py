from django.db import models

from users.models import User
from Recipes.models import Recipe


class ShoppingCart(models.Model):
    """Список покупок пользователя."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='author_shop_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipes_shop_cart'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'recipe'],
                name='UniqueShoppingCart'

            )
        ]

    def __str__(self):
        return self.recipe.name


class Favourites(models.Model):
    """Избранные рецепты."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite_recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipes_fav'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'recipe'],
                name='UniqueFavorite'

            )
        ]

    def __str__(self):
        return self.recipe.name


class Subscription(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriber'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='UniqueSubscribtion'

            )
        ]
