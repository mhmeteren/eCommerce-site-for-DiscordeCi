from rest_framework import status
from rest_framework.response import Response

from UserApp.models import User
from UserApp.api.serializers import UserSerializers

#class views
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404


class UserAccTokenAutAPIView(APIView):
    def get_object(self, token):
        dc_instance = get_object_or_404(User, TOKEN=token)
        return dc_instance


    def get(self, request, token):
        user = self.get_object(token)
        serializer = UserSerializers(user)
        return Response(serializer.data)
