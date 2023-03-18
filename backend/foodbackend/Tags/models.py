from django.db import models


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        'Название',
        max_length=154
    )
    color = models.CharField(
        'Цвет',
        max_length=7
    )
    slug = models.SlugField(
        max_length=64
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
    
    def __str__(self):
        return self.name
