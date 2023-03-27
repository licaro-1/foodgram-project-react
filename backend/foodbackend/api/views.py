from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserChangePasswordSerializer,
    IngredientsSerializer,
    TagsSerializer,
    RecipesListSerializer,
    SubscriptionsSerializer,
    RecipePostSerializer,
    SmallRecipeSerializer
)
from.paginaton import RecipePagination
from .permissions import isAdminOwnerOrReadOnly
from users.models import User
from CapabilitiesUser.models import Subscription, ShoppingCart
from Recipes.models import Recipe, Tag, Ingredient
from .filters import RecipeFilter, IngredientFilter


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class CreateDestroyViewSet(mixins.CreateModelMixin, 
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes_by_action = {
        'create': (AllowAny,),
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'destroy': (isAdminOwnerOrReadOnly,),
        'patch': (isAdminOwnerOrReadOnly,)
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer
        
    @action(
        detail=False,
        methods=['get']
    )
    def me(self, request):
        user = self.request.user
        serializer = UserSerializer(user, context={'request':request})
        return Response(serializer.data)
    
    @action(
        detail=False,
        methods=['post'],
        serializer_class=UserChangePasswordSerializer,
        permission_classes=(isAdminOwnerOrReadOnly,),
    )
    def set_password(self, request):
        user = self.request.user
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            current_password = serializer.validated_data.get(
                'current_password'
            )
            new_password = serializer.validated_data.get(
                'new_password'
            )
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors)
    
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            return [permission() for permission in self.permission_classes]


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredient.objects.all()
    filterset_class = IngredientFilter
    filter_backends = [DjangoFilterBackend]


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesListSerializer
    pagination_class = RecipePagination
    filterset_class = RecipeFilter
    filter_backends = [DjangoFilterBackend, ]
    permission_classes_by_action = {
        'create': (IsAuthenticated,),
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'destroy': (isAdminOwnerOrReadOnly,),
        'patch': (isAdminOwnerOrReadOnly,),
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == ('create' or 'update'):
            return RecipePostSerializer
        return RecipesListSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        recipe = get_object_or_404(Recipe, id=serializer.data['id'])
        instance_serializer = RecipesListSerializer(
            recipe,
            context={'request': request}
        )
        return Response(instance_serializer.data)

    def update(self, request, pk=None, partial=True):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = self.get_serializer(
            data=request.data,
            instance=recipe,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance_serializer = RecipesListSerializer(
            recipe, 
            context={'request': request}
        )
        return Response(instance_serializer.data)


class SubscriptionsListViewSet(ListViewSet):
    serializer_class = SubscriptionsSerializer
    
    def get_queryset(self):
        queryset = Subscription.objects.filter(
            user=self.request.user
        ).all()
        return queryset


class SubscriptionCreateDestroyViewSet(CreateDestroyViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionsSerializer
    lookup_field = 'user_id'

    def create(self, request, user_id=None):
        author = get_object_or_404(
            User,
            id=user_id
        )
        already_subscribed = Subscription.objects.filter(
            author=author,
            user=request.user
        )
        if request.user == author or already_subscribed:
            errors = {'errors': 'Вы уже подписаны или являетесь автором.'}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.create(
            author=author, user=request.user
        )
        result = Subscription.objects.get(author=author, user=request.user)
        serializer = self.get_serializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, user_id=None):
        author = get_object_or_404(User, id=user_id)
        if request.user != author:
            subscribe = get_object_or_404(
                Subscription,
                author=author,
                user=request.user
            )
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        errors = {'errors': 'Вы не подписаны на пользователя или являетесь автором'}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)



class ShoppingCartCreateDestroy(CreateDestroyViewSet):
    serializer_class = SmallRecipeSerializer
    queryset = ShoppingCart.objects.all()

    def create(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        already_created = ShoppingCart.objects.filter(
            author=request.user,
            recipe=recipe
        )
        if not already_created:
            ShoppingCart.objects.create(
                author=request.user,
                recipe=recipe
            )
            serializer = self.get_serializer(recipe)
            return Response(serializer.data)
        error = {'errors': 'Рецепт уже находится в списке покупок'}
        return Response(error)

    def destroy(self, request, pk=None):
        shopp_cart_obj = ShoppingCart.objects.filter(
            id=pk
        )
        if shopp_cart_obj:
            shopp_cart_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        error = {'errors': 'Указанного рецепта нет в списке избранных'}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
