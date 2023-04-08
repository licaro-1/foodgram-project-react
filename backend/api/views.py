from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .paginaton import MainPagination
from .permissions import IsAdminOwnerOrReadOnly, IsAdmin
from users.models import User
from users_capabilities.models import Subscription, ShoppingCart, Favourites
from recipes.models import Recipe, Tag, Ingredient
from .filters import RecipeFilter, IngredientFilter
from api.common.common_viewsets import (CommonUserViewSet,
                                        CommonPermissionByActionViewSet)
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    IngredientsSerializer,
    TagsSerializer,
    RecipesListSerializer,
    SubscriptionsSerializer,
    RecipePostSerializer,
    SmallRecipeSerializer
)
from users_capabilities.services import (
    delete_subscribtion_by_user_and_author,
    create_subscribtion_by_user,
    add_recipe_to_shopping_cart,
    delete_recipe_from_shopping_cart,
    add_recipe_to_favourite,
    revome_recipe_from_favourite
)


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet, CommonUserViewSet,
                  CommonPermissionByActionViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'retrieve']
    pagination_class = MainPagination
    permission_classes_by_action = {
        'create': [AllowAny, ],
        'list': [AllowAny, ],
        'retrieve': [AllowAny, ],
        'destroy': [IsAdmin, ],
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredient.objects.all()
    filterset_class = IngredientFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [AllowAny, ]


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesListSerializer
    pagination_class = MainPagination
    filterset_class = RecipeFilter
    filter_backends = [DjangoFilterBackend, ]
    permission_classes = (IsAdminOwnerOrReadOnly, )
    http_method_names = ['get', 'post', 'patch', 'retrieve', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipePostSerializer
        return RecipesListSerializer

    def update(self, request, pk=None, partial=True):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = self.get_serializer(data=request.data, instance=recipe,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance_serializer = RecipesListSerializer(
            recipe,
            context={'request': request}
        )
        return Response(instance_serializer.data)


class SubscriptionsListViewSet(ListViewSet):
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = MainPagination

    def get_queryset(self):
        queryset = self.request.user.subscriber.all()
        return queryset


class SubscriptionCreateDestroyViewSet(CreateDestroyViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionsSerializer
    lookup_field = 'user_id'

    def create(self, request, user_id=None):
        author = get_object_or_404(User, id=user_id)
        subscribe_create = create_subscribtion_by_user(request.user, author)
        if not subscribe_create:
            errors = {'errors': 'Вы уже подписаны или являетесь автором.'}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(subscribe_create)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, user_id=None):
        author = get_object_or_404(User, id=user_id)
        delete_subscribe = delete_subscribtion_by_user_and_author(
            request.user,
            author)
        if delete_subscribe is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        errors = {
            'errors': 'Вы не подписаны на пользователя или являетесь автором'
        }
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartCreateDestroy(CreateDestroyViewSet):
    serializer_class = SmallRecipeSerializer
    queryset = ShoppingCart.objects.all()

    def create(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        add_to_shop_cart = add_recipe_to_shopping_cart(request.user, recipe)
        if add_to_shop_cart:
            serializer = self.get_serializer(add_to_shop_cart)
            return Response(serializer.data)
        error = {'errors': 'Рецепт уже находится в списке покупок'}
        return Response(error)

    def destroy(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        delete_recipe_from_shop_cart = delete_recipe_from_shopping_cart(
            request.user,
            recipe
        )
        if delete_recipe_from_shop_cart is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        error = {'errors': 'Указанного рецепта нет в списке избранных'}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class FavouritesViewSet(CreateDestroyViewSet):
    queryset = Favourites.objects.all()
    serializer_class = SmallRecipeSerializer

    def create(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        recipe_to_favourite = add_recipe_to_favourite(
            request.user,
            recipe
        )
        if recipe_to_favourite is None:
            serializer = self.get_serializer(recipe)
            return Response(serializer.data)
        error = {'errors': 'Рецепт уже находится в списке избранных'}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        remove_recipe = revome_recipe_from_favourite(request.user, recipe)
        if remove_recipe is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        error = {'error': 'Указанного рецепта нет в списке избранных'}
        return Response(error)
