from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from CapabilitiesUser.models import Subscription, ShoppingCart, Favourites
from users.models import User
from Recipes.models import (Recipe, Tag, Ingredient, RecipeIngredients)


class UserAdmins(UserAdmin):
    """Админка пользователя."""
    model = User
    list_display = ['id', 'username', 'email']
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')


class IngredientsAdmin(admin.ModelAdmin):
    """Админка ингредиентов."""
    list_display = ['name', 'measurement_unit']
    list_filter = ('name',)


class RecipesAdmin(admin.ModelAdmin):
    """Админка рецептов."""
    list_display = ['id', 'name', 'author', 'add_to_favorite_count']
    list_filter = ('author', 'name', 'tags')


admin.site.register(User, UserAdmins)
admin.site.register(Recipe, RecipesAdmin)
admin.site.register(RecipeIngredients)
admin.site.register(Ingredient, IngredientsAdmin)
admin.site.register(Tag)
admin.site.register(Subscription)
admin.site.register(ShoppingCart)
admin.site.register(Favourites)
