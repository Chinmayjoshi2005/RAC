# users/views.py

from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import Group # Import Group

# This is the class that was missing
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# This is the login class
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # --- NEW: Get User Role ---
        user_groups = user.groups.all()
        role = 'student' # Default role
        if user_groups.exists():
            # Assuming user belongs to only one group relevant for dashboard
            group_name = user_groups.first().name.lower()
            if group_name in ['faculty', 'parent']:
                role = group_name
        # --- END OF NEW CODE ---

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'role': role # <-- Send the role back to frontend
        })