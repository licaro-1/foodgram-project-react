from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import TokenCreateView, TokenDestroyView
from Recipes.shop_cart_download import DownloadCart

from .views import (
    UserViewSet,
    IngredientsViewSet,
    TagsViewSet,
    RecipesViewSet,
    SubscriptionsListViewSet,
    SubscriptionCreateDestroyViewSet,
    ShoppingCartCreateDestroy,
    FavouritesViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'recipes', RecipesViewSet)


urlpatterns = [
    path(
        'users/subscriptions/',
        SubscriptionsListViewSet.as_view({'get': 'list'}),
        name='subscribelist'
    ),
    path('users/<int:user_id>/subscribe/',
         SubscriptionCreateDestroyViewSet.as_view({
            'post': 'create', 'delete': 'destroy'
            }),
         name='subscribe'),
    path('recipes/download_shopping_cart/',
         DownloadCart.as_view(), name='download_cart'),
    path('recipes/<int:pk>/shopping_cart/',
         ShoppingCartCreateDestroy.as_view({
             'delete': 'destroy', 'post': 'create'
            })),
    path('recipes/<int:pk>/favorite/',
         FavouritesViewSet.as_view({'delete': 'destroy', 'post': 'create'})),
    path('', include(router.urls)),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
]