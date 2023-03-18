from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from CapabilitiesUser.models import Subscription, ShoppingCart
from Ingredients.models import Ingredient
from Tags.models import Tag
from Recipes.models import Recipe


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
    
    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        print(request)
        if request.user.is_authenticated and obj.username != request.user.username:
            author = User.objects.filter(username=obj.username)
            subscribe_checker = Subscription.objects.filter(
                user = request.user,
                author=author[0]
            )
            return len(subscribe_checker) != 0
        return False


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        max_length=150
    )
    current_password = serializers.CharField(
        max_length=150
    )


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class RecipesSerializer(serializers.ModelSerializer):
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    tags = TagsSerializer(many=True)
    ingredients = IngredientsSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_in_shopping_cart(self, obj):
        """Проверка на вхождение рецепта в список покупок."""
        print(obj)
        if self.request.user.is_authenticated:
            recipe = Recipe.objects.filter(id=obj.id)
            recipe_in_shop_cart = recipe.recipes.filter(
                author=self.request.user
            )
            if len(recipe_in_shop_cart) != 0:
                return True
        return False

    def is_favorited(self, obj):
        """Проверка на вхождение рецепта в список избранных."""
        if self.request.user.is_authenticated:
            recipe = Recipe.objects.filter(id=obj.id)
            recipe_is_favorited = recipe.recipes_fav.filter(
                user=self.request.user
            )
            if len(recipe_is_favorited) != 0:
                return True
        return False
            



# class SubscriptionsSerializer(serializers.ModelSerializer):
#     recipes = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=Recipe.objects.all()
#     )

#     class Meta:
#         model = Subscription
#         field = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'recipes',
#             'recipes_count'
#         )


