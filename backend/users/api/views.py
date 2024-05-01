from rest_framework import generics

from users.api.serializers import UserSerializer


class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
