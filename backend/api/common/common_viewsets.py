from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import UserSerializer, UserChangePasswordSerializer
from ..permissions import IsAdminOrAuthor


class CommonUserViewSet(viewsets.ViewSet):
    """
    Общий вьюсет пользователя с методами изменения
    пароля и отображения личной информации.
    """

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAdminOrAuthor, ]
    )
    def me(self, request):
        user = self.request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        serializer_class=UserChangePasswordSerializer,
        permission_classes=(IsAdminOrAuthor,),
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
        errors = {'errors': 'Неверный пароль'}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class CommonPermissionByActionViewSet(viewsets.ViewSet):

    def get_permissions(self):
        try:
            return [permission() for permission
                    in self.permission_classes_by_action[self.action]]
        except KeyError:
            if self.action:
                action_func = getattr(self, self.action, {})
                action_func_kwargs = getattr(action_func, 'kwargs', {})
                permission_classes = action_func_kwargs.get(
                    'permission_classes'
                )
            else:
                permission_classes = None

            return [permission() for permission
                    in (permission_classes or self.permission_classes)]
