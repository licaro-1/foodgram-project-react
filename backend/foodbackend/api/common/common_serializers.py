import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from Recipes.models import Recipe
from users.models import User
from CapabilitiesUser.models import Subscription


class ImageField(serializers.ImageField):
    """Поле для изображения."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IsFavAndInShopCart(serializers.Serializer):
    """
    Общий сериализатор с проверочными методами (в списке покупок, в избранном).
    """
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


class IsSubscribed(serializers.Serializer):
    """
    Общий сериализатор с проверочным методом (подписан на пользователя).
    """
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context['request']
        if isinstance(obj, User):
            user_id = obj.id
        elif isinstance(obj, dict):
            return obj['is_subscribed']
        else:
            user_id = obj.author.id
        author = get_object_or_404(User, id=user_id)
        if request.user.is_authenticated and author != request.user:
            subscribe_checker = Subscription.objects.filter(
                user=request.user,
                author=author
            )
            if subscribe_checker:
                return True
        return False
