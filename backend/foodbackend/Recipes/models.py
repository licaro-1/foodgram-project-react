from django.db import models
from django.core.validators import MinValueValidator

from users.models import User
from Ingredients.models import Ingredient
from Tags.models import Tag


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipe_author'
    )
    title = models.CharField(
        'Название',
        max_length=120
    )
    ingrediens = models.ForeignKey(
        Ingredient, 
        on_delete=models.SET_NULL,
        verbose_name='Ингредиенты',
        null=True
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

    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        verbose_name='Тэг',
        null=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title