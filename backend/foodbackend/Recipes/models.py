import re

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        'Название',
        max_length=150
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=50
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


def validate_color(value):
    color_is_hex = re.match('^#(?:[0-9a-fA-F]{3}){1,2}$', value)
    if not color_is_hex:
        raise ValidationError('Цвет должен быть формата HEX')
    return value


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        'Название',
        max_length=154,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        validators=[validate_color]
    )
    slug = models.SlugField(
        max_length=64
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipe_author'
    )
    name = models.CharField(
        'Название',
        max_length=120
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты'
    )
    text = models.TextField(
        'Описание'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipe/',
        blank=True
    )
    cooking_time = models.IntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1)]
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
        related_name='tags'
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created',)

    def __str__(self):
        return self.name

    @property
    def add_to_favorite_count(self):
        recipe = get_object_or_404(Recipe, id=self.id)
        return recipe.recipes_fav.all().count()

    add_to_favorite_count.fget.short_description = 'Кол-во добавлений \
                                                    в избранное'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='UniqueIngredientRecipe'

            )
        ]

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'
