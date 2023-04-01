from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import UserSerializer, UserChangePasswordSerializer
from ..permissions import isAdminOwnerOrReadOnly


class CommonUserViewSet(viewsets.ViewSet):
    """
    Общий вьюсет пользователя с методами изменения 
    пароля и отображения личной информации.
    """

    @action(
        detail=False,
        methods=['get']
    )
    def me(self, request):
        user = self.request.user
        serializer = UserSerializer(user, context={'request': request})
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
