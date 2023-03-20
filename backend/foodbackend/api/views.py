from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserChangePasswordSerializer,
    IngredientsSerializer,
    TagsSerializer,
    RecipesSerializer
)
from .permissions import isAdminOwnerOrReadOnly, IsAdmin

from users.models import User
from CapabilitiesUser.models import Subscription
from Recipes.models import Recipe, Tag, Ingredient


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {
        'create': (AllowAny,),
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'destroy': (IsAdmin,),
        'patch': (IsAdmin,)
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
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredient.objects.all()


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


# class SubscriptionsViewSet(viewsets.ModelViewSet):

#     def get_queryset(self):
#         queryset = Subscription.objects.filter(
#             user=self.request.user
#         )
#         return queryset
#     pass


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [AllowAny,]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}