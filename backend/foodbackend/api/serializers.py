import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from CapabilitiesUser.models import Subscription
from Recipes.models import Recipe, Tag, Ingredient, RecipeIngredients
from .common.common_serializers import (ImageField,
                                        IsFavAndInShopCart,
                                        IsSubscribed)
from Recipes.services import create_update_recipe_tags_ingredients


class UserSerializer(serializers.ModelSerializer, IsSubscribed):
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
            'is_subscribed',
            'password'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }


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


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class IngredientAmountRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )
        extra_kwargs = {
            'name': {'required': False},
            'slug': {'required': False},
            'color': {'required': False}
        }

    def validate_color(self, value):
        color = re.match('^#(?:[0-9a-fA-F]{3}){1,2}$', value)
        if not color:
            raise serializers.ValidationError('Цвет должен быть формата HEX')
        return value


class RecipesListSerializer(serializers.ModelSerializer, IsFavAndInShopCart):
    author = UserSerializer(read_only=True)
    tags = TagsSerializer(many=True)
    ingredients = RecipeIngredientsSerializer(
        source='recipe_ingredients',
        many=True
    )
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
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


class SmallRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class RecipePostSerializer(serializers.ModelSerializer, IsFavAndInShopCart):
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountRecipeSerializer(
        source='recipe_ingredients',
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = ImageField(required=False)

    class Meta:
        model = Recipe
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
            'cooking_time',
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe_ingredients')
        
        recipe = Recipe.objects.create(**validated_data)
        for tag_obj in tags:
            recipe.tags.add(tag_obj)
            recipe.save()
        for ingredient in ingredients:
            ingedients = RecipeIngredients.objects.create(
                ingredient_id=ingredient['ingredient']['id'],
                recipe=recipe,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)
        tags_list = validated_data.get('tags')
        ingredients_list = validated_data.get('recipe_ingredients')
        create_update_recipe_tags_ingredients(
            instance,
            tags_list,
            ingredients_list
        )
        instance.save()
        return instance


class SubscriptionsSerializer(serializers.ModelSerializer, IsSubscribed):
    id = serializers.ReadOnlyField(source='author.id')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        recipes_count = obj.author.recipe_author.count()
        return recipes_count

    def get_recipes(self, obj):
        request = self.context['request']
        limit_recipes_value = request.GET.get('recipes_limit')
        if limit_recipes_value:
            queryset = Recipe.objects.all().filter(
                author__id=obj.author.id
            )[:int(limit_recipes_value)]
        else:
            queryset = Recipe.objects.filter(author__id=obj.author.id).all()
        serializer = SmallRecipeSerializer(queryset, many=True)
        return serializer.data
