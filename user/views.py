from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerialize, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """ creating a new user in the system """
    serializer_class = UserSerialize

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES



class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the auth """
    serializer_class = UserSerialize
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user
